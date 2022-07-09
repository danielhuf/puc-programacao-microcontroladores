#include <AFMotor.h>

#define VEL 160

int sensorOtico = A11;
int sensorOtico2 = A12;

int sensorEsq;
int sensorDir;

unsigned long instanteAnterior = 0;
unsigned long instanteAtual = 0;

boolean Auto = false;

AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  Serial1.begin(9600);
  Serial1.setTimeout(10);

  pinMode(sensorOtico, INPUT);
  pinMode(sensorOtico2, INPUT);
}

void loop() {
  instanteAtual = millis();
  sensorEsq = digitalRead(sensorOtico);
  sensorDir = digitalRead(sensorOtico2);
  if (instanteAtual >= instanteAnterior + 100) {
    Serial.println(String(sensorEsq) + " " + String(sensorDir));
    Serial1.println(String(digitalRead(sensorOtico))+" " +String(digitalRead(sensorOtico2)));
    instanteAnterior = instanteAtual;
  }

  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();
    if (!Auto) {
      if (texto == "frente") {
        frente();
      }
      else if (texto == "tras") {
        tras();
      }
      else if (texto == "direita") {
        direita();
      }
      else if (texto == "esquerda") {
        esquerda();
      }
    }
    if (texto == "parar") {
      parar();
      Auto = false;
    }
    else if (texto == "auto") {
      Auto = true;
    }
  }

  if (Auto) {
    if (sensorEsq && sensorDir) {
      frente();
    }
    else if (!sensorEsq && !sensorDir) {
      tras();
    }
    else if (!sensorEsq && sensorDir) {
      direita();
    }
    else if (sensorEsq && !sensorDir) {
      esquerda();
    }
  }
}

void frente() {
  motor3.run(FORWARD);
  motor3.setSpeed(VEL);
  motor4.run(FORWARD);
  motor4.setSpeed(VEL);
}

void tras() {
  motor3.run(BACKWARD);
  motor3.setSpeed(VEL);
  motor4.run(BACKWARD);
  motor4.setSpeed(VEL);
}

void esquerda() {
  motor3.run(RELEASE);
  motor4.run(FORWARD);
  motor4.setSpeed(VEL);
}

void direita() {
  motor4.run(RELEASE);
  motor3.run(FORWARD);
  motor3.setSpeed(VEL);
}

void parar() {
  motor4.run(RELEASE);
  motor3.run(RELEASE);
}
