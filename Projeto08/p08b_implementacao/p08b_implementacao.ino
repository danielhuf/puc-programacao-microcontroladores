#include <GFButton.h>
#include <EEPROM.h>
#include <Servo.h>
#include <meArm.h>

// braco
int base = 12, ombro = 11, cotovelo = 10, garra = 9;
bool aberto = true;
bool absoluto = true; // relativo == false
int X = 0, Y = 130, Z = 0;

// joystick
int eixoX = A0;
int eixoY = A1;

int potenciometro = A5;

// botoes
GFButton botaoA(2);
GFButton botaoB(3);
GFButton botaoC(4);

meArm braco(
  180, 0, -pi / 2, pi / 2, // ângulos da base
  135, 45, pi / 4, 3 * pi / 4, // ângulos do ombro
  180, 90, 0, -pi / 2, // ângulos do cotovelo
  30, 0, pi / 2, 0 // ângulos da garra
);

void setup() {
  Serial.begin(9600);

  // braco
  braco.begin(base, ombro, cotovelo, garra);
  braco.gotoPoint(X, Y, Z);
  braco.openGripper();
  Serial.println("Modo absoluto");

  // joystick
  pinMode(eixoX, INPUT);
  pinMode(eixoY, INPUT);

  // potenciometro
  pinMode(potenciometro, INPUT);

  // botao
  botaoA.setPressHandler(mudaEstadoGarra);
  botaoB.setPressHandler(mudaModo);
}

void loop() {
  botaoA.process();
  botaoB.process();
  botaoC.process();

  if (absoluto)
    modoAbsoluto();
  else
    modoRelativo();
}

void mudaEstadoGarra() {
  aberto = !aberto;

  if (aberto) {
    braco.openGripper();
  } else {
    braco.closeGripper();
  }
}

void mudaModo() {
  absoluto = !absoluto;
  if (absoluto)
    Serial.println("Modo absoluto");
  else
    Serial.println("Modo relativo");
}

void modoAbsoluto() {
  X = map(analogRead(eixoX) , 0, 1023, -150, 150);
  Y = map(analogRead(eixoY) , 0, 1023, 100, 200);
  Z = map(analogRead(potenciometro) , 0, 1023, -30, 100);
  braco.gotoPoint(X, Y, Z);
}

void modoRelativo() {
  X += map(analogRead(eixoX) , 0, 1023, -10, 10);
  Y += map(analogRead(eixoY) , 0, 1023, -10, 10) + 1;
  Z = map(analogRead(potenciometro) , 0, 1023, -30, 100);

  X = constrain(X, -150, 150);
  Y = constrain(Y, 100, 200);

  Serial.print(X);
  Serial.print( " // " );
  Serial.print(Y);
  Serial.print( " // " );
  Serial.println(Z);

  braco.goDirectlyTo(X, Y, Z);
  delay(50);
}
