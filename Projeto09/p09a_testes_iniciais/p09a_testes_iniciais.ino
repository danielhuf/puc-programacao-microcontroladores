#include <AFMotor.h>

int sensorOtico = A11;
int sensorOtico2 = A12;
bool claro = true;
int n;
int valorAnteriorSensor;
AF_DCMotor motor3(3);
int contagem = 0;

void setup() {
  pinMode(sensorOtico, INPUT);
  pinMode(sensorOtico2, INPUT);
  Serial.begin(9600);
  Serial.setTimeout(10);
  valorAnteriorSensor = analogRead(sensorOtico2);
}

void loop() {
  if ((digitalRead(sensorOtico) == LOW && !claro) || (digitalRead(sensorOtico) == HIGH && claro)) {
    claro = !claro;
    Serial.println("mudou");
  }
  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();
    if (texto.startsWith("frente")) {
      motor3.run(FORWARD);
      n = texto.substring(7).toInt();
      motor3.setSpeed(n);
    }
    else if (texto.startsWith("tras")) {
      motor3.run(BACKWARD);
      n = texto.substring(5).toInt();
      motor3.setSpeed(n);
    }
  }
  int valorAtualSensor = analogRead(sensorOtico2);
  if (valorAtualSensor > 800 && valorAnteriorSensor < 800) {
    contagem++;
    Serial.println("contagem " + String(contagem));
  }
  valorAnteriorSensor = valorAtualSensor;
}
