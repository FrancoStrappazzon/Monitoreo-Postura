import serial
import cv2
import re
import time
import pandas as pd
from database import insert_data, fetch_data  # Importo la función para insertar datos


#funcion para configurar el puerto serial
def config_serial():
    try:
        return serial.Serial('COM6', 115200)
    except serial.SerialException as e:
        print(f"Error abriendo el puerto serial: {e}")
        return None


#funcion para chequear la postura evaluando el rostro mediante la camara
def check_posture():
    ret, frame = cap.read()  # Capturo imagen de la cámara
    if not ret:
        print("No se pudo capturar la imagen de la cámara.")
        return False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convierto la imagen a escala de grises

    # Cargo el clasificador de rostros
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("No se pudo cargar el clasificador de rostros.")
        exit()


    # Detecto rostro
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    posture_status = True  # Por defecto, asumir postura correcta
    for (x, y, w, h) in faces:
        # Dibujo un rectángulo alrededor del rostro
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Evaluo la posición y tamaño del rostro
        if y > 200 or h > 200:  # Ajustar estos valores según la posición de la cámara y la distancia esperada
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # usa formato BGR (blue, green, red)
            ser.write(b"INCLINACION_INCORRECTA\n")  # Enviar comando a la ESP32
            cv2.imshow('Postura', frame)
            posture_status = False
        else:
            ser.write(b"INCLINACION_CORRECTA\n")  # Enviar comando a la ESP32
            cv2.imshow('Postura', frame)

    return posture_status


#funcion para exportar archivo csv cuando aprieto el pulsador
def export_data_to_csv():
    data = fetch_data()  # Obtengo los datos de la base de datos
    df = pd.DataFrame(data, columns=["id", "timestamp", "distancia", "posture_status"])
    df.to_csv('datos_postura.csv', index=False)
    print("Datos exportados a 'datos_postura.csv' ")


#funcion para seguir leyendo el puerto serie en caso de presionar el pulsador mientras espero una nueva deteccion de rostro
def monitor_serial_input(duracion_segundos):
    ser = config_serial()
    start_time = time.time()
    while time.time() - start_time < duracion_segundos:
        if ser.in_waiting > 0:
            # Leo la línea completa desde el puerto serie
            line = ser.readline().decode('utf-8').strip()
            print(f"Mensaje recibido {line}")

            if "EXPORT_DATA" in line:
                print("Exportando datos")
                export_data_to_csv()

        # Salir del loop con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)  # Pequeña espera para evitar sobrecargar la CPU
    print("Tiempo de espera completado")


#bucle principal
while True:
    ser = config_serial()  # Configura el puerto serial

    # Verifico si el puerto serial fue configurado correctamente
    if ser is None:
        print("Error al configurar el puerto serial. Saliendo...")
        break

    # Inicializo la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        ser.close()
        exit()

    start_time = time.time()  # arranco a contar
    while time.time() - start_time < 20:

        if ser.in_waiting > 0:
            # Leo la línea completa desde el puerto serie
            line = ser.readline().decode('utf-8').strip()
            print(f"Mensaje recibido {line}")

            if "EXPORT_DATA" in line:
                print("Exportando datos")
                export_data_to_csv()

            # Extraer la distancia usando una expresión regular
            match = re.search(r'Distancia: (\d+) cm', line)

            if match:
                distance = int(match.group(1))  # Convierto el valor a entero
                print(f"Distancia: {distance} cm")

                # Verifico la postura con OpenCV
                posture_status = check_posture()
                # Inserto los datos a la base de datos
                insert_data(distance, posture_status)

                if posture_status and 45 <= distance <= 65:
                    print("Postura y distancia correctas.")
                else:
                    print("Necesitas corregir tu postura o distancia.")
            else:
                print("No se pudo encontrar una distancia válida en la cadena recibida.")

        # Salir del loop con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Limpio recursos
    cap.release()
    cv2.destroyAllWindows()
    ser.close()

    # Temporizador que escucha el puerto serial durante 2 minutos
    monitor_serial_input(120)  # Aquí espera pero sigue verificando el puerto serie
    