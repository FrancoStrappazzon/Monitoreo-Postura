#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Definir los pines de TRIG y ECHO del sensor
const int trigPin = 5;
const int echoPin = 18;

// Pulsador para exportar archivo CSV
const int pulsador = 23; 

// Variables para almacenar el tiempo y la distancia
long duration;
int distance;

// Ancho y alto del display OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// LED de alarma
#define LED_PIN 4

// Creo una instancia para el display
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

volatile bool exportDataFlag = false;  // Variable para indicar la solicitud de exportación

void setup() {
  // Inicializar el monitor serial
  Serial.begin(115200);
  //configuro pines led y pulsador
  pinMode(LED_PIN, OUTPUT);
  pinMode(pulsador, INPUT_PULLUP);

  // Configurar interrupción para el pulsador
  attachInterrupt(digitalPinToInterrupt(pulsador), exportData, FALLING);  // Activa la interrupción en FALLING (flanco de bajada)

  // Inicializar el display OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {  // Dirección 0x3C para SSD1306
    Serial.println(F("No se encuentra el OLED!"));
    while(true);
  }

  // Configuro los pines TRIG y ECHO del sensor de ultrasonido
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Limpiar el buffer del display
  display.clearDisplay();

  // Configurar color de texto
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(0,10);
  display.println(F("Distancia: "));
}

void loop() {
  // Si la bandera de exportación está activada, envio el comando por el puerto serie
  if (exportDataFlag) {
    Serial.print("EXPORT_DATA");  // Envío comando para exportar los datos
    exportDataFlag = false;  // Reinicio la bandera
  }

  // Me aseguro de que el pin TRIG esté en LOW
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Envio un pulso de 10us en el pin TRIG
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Leo el tiempo de duración del pulso en el pin ECHO
  duration = pulseIn(echoPin, HIGH);

  // Calculo la distancia en cm
  distance = duration * 0.034 / 2;

  // Limpiar el display
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(0,10);

//Si detecta distancias muy grandes no le hago caso
  if(distance <= 100){
    Serial.print("Distancia: ");
    Serial.print(distance);
    Serial.println(" cm");

//Distancia valida para una correcta postura
    if(distance < 45 || distance > 65){
      display.println("Corregir  distancia");
      display.display();
      digitalWrite(LED_PIN, HIGH);  // Enciende el LED
    }
    else{
      display.println("Distancia:" + String(distance) + "cm");
      display.display();
      digitalWrite(LED_PIN, LOW);   // Apaga el LED
    }
    delay(2000);  // Espero un momento antes de la siguiente medición
  }

  // Verifico si la inclinación de mi cuerpo es correcta mediante un valor que ingresa por el puerto serie
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command == "INCLINACION_INCORRECTA") {
      digitalWrite(LED_PIN, HIGH);  // Enciende el LED
    } else if (command == "INCLINACION_CORRECTA") {
      digitalWrite(LED_PIN, LOW);   // Apaga el LED
    }
  }
}

// Función de interrupción para el pulsador
void exportData() {
  exportDataFlag = true;  // Activar la bandera para exportar datos
}
