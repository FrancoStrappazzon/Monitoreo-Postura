# Sistema de Monitoreo de Postura con ESP32 y Python

Este proyecto implementa un sistema de monitoreo de postura utilizando una ESP32 con un sensor de ultrasonido y un script de Python que analiza la postura del usuario mediante OpenCV. La detección de la postura se realiza cada cierto intervalo de tiempo, y los datos recolectados se guardan en una base de datos MySQL para su posterior análisis.

## Características

- **Monitoreo de distancia:** Utiliza un sensor de ultrasonido conectado a la ESP32 para medir la distancia del usuario a la pantalla.
- **Detección de postura:** Utiliza OpenCV para detectar la postura del usuario basándose en la posición del rostro.
- **Alerta de corrección de postura:** Si se detecta una postura incorrecta o la distancia no es la adecuada, el sistema emite una alerta.
- **Exportación de datos:** Un botón/pulsador permite exportar los datos recolectados a un archivo CSV para análisis y visualización con Python.
- **Interacción con una base de datos MySQL:** Los datos se almacenan en una base de datos MySQL.

## Requisitos

- **Hardware:**
  - ESP32
  - Sensor de Ultrasonido HC-SR04
  - Cámara web
  - Pulsador
  - Pantalla Oled 0.96p I2c 128x64
  - Led rojo

- **Software:**
  - Python 3.x
  - Librerías de Python: `opencv-python`, `pyserial`, `pandas`, `mysql-connector-python`
  - Arduino IDE para programar la ESP32
  - Servidor MySQL instalado

![monitoreo_postura](https://github.com/user-attachments/assets/cf3e27aa-dbb8-48d8-b08f-ce58a3e5ac89)

![monitoreo_postura3](https://github.com/user-attachments/assets/7f4ef0ec-9f5b-4b63-9fc1-c224e8386e6b)

![monitoreo_postura5](https://github.com/user-attachments/assets/dbc6faf7-ba9d-484e-bb2d-4f4923bec35b)

![image](https://github.com/user-attachments/assets/3dd8c36f-a5df-4716-9154-ab31701b15c9)

