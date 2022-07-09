
#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

RotaryEncoder encoder(20, 21);

GFButton botao1(A1);
GFButton botao2(A2);
ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

int campainhaPassiva = 5;
int sensorDeSom = 19;
int leds[] = {13, 12, 11, 10};
int estalar = 0;

unsigned long instanteAnterior = 0;
unsigned long instanteAnterior2 = 0;
int posicaoAnterior = 0;

void setup() {
    botao1.setPressHandler(toca1);
    botao2.setPressHandler(toca2);
    botao2.setReleaseHandler(solta2);
    pinMode(A5, OUTPUT);
    digitalWrite(A5, LOW);

    for (int i = 0; i < 4; i++){
      pinMode(leds[i], OUTPUT);
      digitalWrite(leds[i], HIGH);
    }

    pinMode(sensorDeSom, INPUT);
    int origem = digitalPinToInterrupt(sensorDeSom);
    attachInterrupt(origem, attEstalo, RISING);
    display.set(estalar);

    int origem1 = digitalPinToInterrupt(20);
    attachInterrupt(origem1, tickDoEncoder, CHANGE);
    int origem2 = digitalPinToInterrupt(21);
    attachInterrupt(origem2, tickDoEncoder, CHANGE);
    
    Serial.begin(9600); 
}

void loop() {
    botao1.process();
    botao2.process();

    display.update();
    unsigned long instanteAtual2 = millis();
    if(instanteAtual2 >= instanteAnterior2 + 500){
      Serial.println(estalar);
      instanteAnterior2 = instanteAtual2;
    }

    int posicao = encoder.getPosition();
    if (posicao != posicaoAnterior){
      digitalWrite(leds[abs(posicaoAnterior%4)], HIGH);
      digitalWrite(leds[abs(posicao%4)], LOW);
      posicaoAnterior = posicao;
    }
}

void toca1(GFButton& botao) {
  tone(campainhaPassiva, 440, 500);
}

void toca2(GFButton& botao){
  tone(campainhaPassiva, 220);
}

void solta2(GFButton& botao){
  noTone(campainhaPassiva);
}

void attEstalo(){
  unsigned long instanteAtual = millis();
  if(instanteAtual > instanteAnterior + 10){
    estalar++;
    display.set(estalar);
    instanteAnterior = instanteAtual;
  }
}

void tickDoEncoder() {
 encoder.tick();
}
