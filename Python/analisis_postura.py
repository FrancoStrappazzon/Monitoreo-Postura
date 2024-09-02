import serial
import cv2
import re
import time
import pandas as pd
from database import insert_data, fetch_data #importo la funcion para insertar datos


def config_serial():
    return serial.Serial('COM6', 115200)  


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
            #print("Advertencia: Parece que te estás encorvando o inclinando demasiado cerca de la pantalla.")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)   #usa formato BGR(blue, green, red)
            ser.write(b"INCLINACION_INCORRECTA\n")  # Enviar comando a la ESP32
            cv2.imshow('Postura', frame)
            posture_status = False
        else:
            ser.write(b"INCLINACION_CORRECTA\n")  # Enviar comando a la ESP32
            cv2.imshow('Postura', frame)
            
    return posture_status

def export_data_to_csv():
    data = fetch_data() #obtengo los datos de la base de datos
    df = pd.DataFrame(data, columns=["id","timestamp","distancia","posture_status"])  
    df.to_csv('datos_postura.csv', index=False)
    print("Datos exportados a 'datos_postura.csv' ")



while True:
    ser = config_serial()  # Configura el puerto serial
    
    # Inicializo la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        exit()
    
    start_time = time.time()    #arranco a contar
    while time.time() -start_time < 20:
        
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

            # Verificar la postura con OpenCV
                posture_status = check_posture()
            #inserto los datos a la base de datos
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

# Limpiar recursos
    cap.release()
    cv2.destroyAllWindows()
    ser.close()

    time.sleep(120)  # Espera 2 minutos antes de la siguiente detección

