#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


// Definir los pines de TRIG y ECHO del sensor
const int trigPin = 5;
const int echoPin = 18;

// Variables para almacenar el tiempo y la distancia
long duration;
int distance;
//Ancho y alto del display OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
//led de alarma
#define LED_PIN 4


// Crear una instancia para el display (Dirección I2C 0x3C)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


void setup() {
  // Inicializar el monitor serial
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);

  // Inicializar el display OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {  // Dirección 0x3C para SSD1306
    Serial.println(F("No se encuentra el OLED!"));
    while(true);
  }


  // Configurar los pines TRIG y ECHO
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

      // Limpiar el buffer del display
  display.clearDisplay();

  // Configurar color de texto
  display.setTextColor(SSD1306_WHITE);

  // Configurar tamaño de texto
  display.setTextSize(2);

  // Configurar la posición del cursor
  display.setCursor(0,10);

  // // Mostrar un mensaje en la pantalla
  display.println(F("Distancia: "));

}

void loop() {
  // Asegurarse de que el pin TRIG esté en LOW
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Enviar un pulso de 10us en el pin TRIG
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Leer el tiempo de duración del pulso en el pin ECHO
  duration = pulseIn(echoPin, HIGH);

  // Calcular la distancia en cm
  distance = duration * 0.034 / 2;
  
  display.clearDisplay();
  // Configurar color de texto
  display.setTextColor(SSD1306_WHITE);

  // Configurar tamaño de texto
  display.setTextSize(2);

  // Configurar la posición del cursor
  display.setCursor(0,10);
   

  if(distance <= 100){
  // Mostrar la distancia en el monitor serial
    Serial.print("Distancia: ");
    Serial.print(distance);
    Serial.println(" cm");

    // Mostrar un mensaje en la pantalla
    display.println("Distancia:" + String(distance) + "cm");
    // Enviar el contenido al display
    display.display();
  // Esperar un momento antes de la siguiente medición
    delay(2000);
  }

//Verifico si la inclinacion de mi cuerpo es correcta mediante un valor que ingresa por el puerto serie
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command == "INCLINACION_INCORRECTA") {
      digitalWrite(LED_PIN, HIGH);  // Enciende el LED
    } else if (command == "INCLINACION_CORRECTA") {
      digitalWrite(LED_PIN, LOW);   // Apaga el LED
    }
  }
}