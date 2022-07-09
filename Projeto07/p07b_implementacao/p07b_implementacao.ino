#include <ShiftDisplay.h>
#include <GFButton.h>
#include <RotaryEncoder.h>

char* nomeDasNotas[] = {"DO ", "REb", "RE ", "MIb", "MI ", "FA ", "SOb", "SOL", "LAb", "LA ", "SIb", "SI "};
int frequencias[] = {131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247};
int campainhaPassiva = 5;
int notaAtual = 0;
int posicaoAnterior = 0;
unsigned long instanteAtual = 0;
unsigned long instanteDepois = 0;
unsigned long instanteAnterior2 = 0;
unsigned long intervalo = 0;
int modo;

GFButton botao1(A1);
GFButton botao2(A2);
ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);
RotaryEncoder encoder(20, 21);

void setup() {
    pinMode(A5, OUTPUT);
    digitalWrite(A5, LOW);

    botao1.setPressHandler(modoAfinador);
    botao1.setReleaseHandler(paraAfinador);

    botao2.setPressHandler(modoMetronomo);
    botao2.setReleaseHandler(paraMetronomo);

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
    Serial.println(notaAtual);

    int posicao = encoder.getPosition();
    if (posicao != posicaoAnterior && modo == 1){
      if (posicao > 11) {
        encoder.setPosition(11);
        posicao = 11;
      }
      else if (posicao < 0) {
        encoder.setPosition(0);
        posicao = 0;
      }
      notaAtual = posicao;
      posicaoAnterior = posicao;
      tocaNota(notaAtual, 200);
    }

    unsigned long instanteAtual2 = millis();
    if(instanteAtual2 >= instanteAnterior2 + intervalo && intervalo != 0 && modo == 2){
      tone(campainhaPassiva, 220, 200);
      instanteAnterior2 = instanteAtual2;
    }
}

void tocaNota(int indiceNota, int duracao) {
  if (duracao < 0) {
    tone(campainhaPassiva, frequencias[indiceNota]);
  }
  else {
    tone(campainhaPassiva, frequencias[indiceNota], duracao);
  }
  display.set(nomeDasNotas[indiceNota]);
}

void modoAfinador(GFButton& botao) {
  modo = 1;
  intervalo = 0;
  tocaNota(notaAtual, -1);
}

void paraAfinador(GFButton& botao) {
  noTone(campainhaPassiva);
  //display.set("");
}

void modoMetronomo(GFButton& botao) {
  modo = 2;
  intervalo = 0;
  instanteAtual = millis();
}

void paraMetronomo(GFButton& botao) {
  instanteDepois = millis();
  intervalo = instanteDepois - instanteAtual;
  int batidasPorMinuto = 60000 / intervalo;
  display.set(batidasPorMinuto);
}

void tickDoEncoder() {
 encoder.tick();
}
