#include <GFButton.h>
#include <EEPROM.h>
#include <Servo.h>

Servo servo1, servo2;
int pinoDoServo1 = 12;
int pinoDoServo2 = 11;
int contBotaoB = 0;
int endereco = 0;
int potenciometro = A5;
int valorAnalogico, anguloEmGraus;
int anguloOmbro = 90;
GFButton botaoA(2);
GFButton botaoB(3);
GFButton botaoC(4);

void setup() {
  Serial.begin(9600);
  servo1.attach(pinoDoServo1);
  servo2.attach(pinoDoServo2);
  pinMode(potenciometro, INPUT);
  EEPROM.get(endereco, contBotaoB);
  Serial.println(contBotaoB);
  botaoB.setPressHandler(aumentaContB);
}

void loop() {
  botaoA.process();
  botaoB.process();
  botaoC.process();
  valorAnalogico = analogRead(potenciometro);
  anguloEmGraus = map(valorAnalogico, 0, 1023, 0, 180);
  // Serial.println(anguloEmGraus);
  servo1.write(anguloEmGraus);
  if (botaoA.isPressed())
    diminuiAngulo();
  if (botaoC.isPressed())
    aumentaAngulo();
}

void aumentaContB() {
  contBotaoB++;
  EEPROM.put(endereco, contBotaoB);
  Serial.println(contBotaoB);
}

void diminuiAngulo() {
  anguloOmbro -= 5;
  if (anguloOmbro < 45)
    anguloOmbro = 45;
  servo2.write(anguloOmbro);
  delay(100);
}

void aumentaAngulo() {
  anguloOmbro += 5;
  if (anguloOmbro > 135)
    anguloOmbro = 135;
  servo2.write(anguloOmbro);
  delay(100);
}
