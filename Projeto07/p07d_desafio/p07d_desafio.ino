// COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
// DEPOIS FAÇA OS NOVOS RECURSOS

#include <ShiftDisplay.h>
#include <GFButton.h>
#include <RotaryEncoder.h>

// 16 notas
int indicesDeNotaDaMusica[] = {7, 2, 0, 11, 9, 7, 2, 0, 11, 9, 7, 2, 0, 11, 0, 9};
int oitavasDaMusica[] = {0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0};
unsigned long intervalosEntreNotas[] = {1000, 1000, 167, 167, 167, 1000, 500, 167, 167, 167, 1000, 500, 167, 167, 167, 1000};

char* nomeDasNotas[] = {"DO ", "REb", "RE ", "MIb", "MI ", "FA ", "SOb", "SOL", "LAb", "LA ", "SIb", "SI "};
int frequencias[] = {131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247};
int campainhaPassiva = 5;
int notaAtual = 0;
int posicaoAnterior = 0;
int oitavaAtual = 0;
int indTempoAtual;
int sensorDeSom = 19;


unsigned long instanteAnterior = -1;
unsigned long intervalos[100];
int totalDeEstalos;
int indiceDoEstaloAtual;
boolean gravando = false;


unsigned long instanteDepois = 0;
unsigned long instanteAnterior2 = 0;
unsigned long instanteAnterior3 = 0;
unsigned long intervalo = 0;
int modo;

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);
ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);
RotaryEncoder encoder(20, 21);

void setup() {
    pinMode(A5, OUTPUT);
    digitalWrite(A5, LOW);

    botao1.setPressHandler(modoAfinador);
    botao1.setReleaseHandler(paraAfinador);
    botao2.setPressHandler(modoEstalo);
    botao3.setPressHandler(tocaMusica);

    int origem1 = digitalPinToInterrupt(20);
    attachInterrupt(origem1, tickDoEncoder, CHANGE);
    int origem2 = digitalPinToInterrupt(21);
    attachInterrupt(origem2, tickDoEncoder, CHANGE);

    pinMode(sensorDeSom, INPUT);
    int origem = digitalPinToInterrupt(sensorDeSom);
    attachInterrupt(origem, attEstalo, RISING);
    
    Serial.begin(9600); 
}

void loop() {
    botao1.process();
    botao2.process();
    botao3.process();
    display.update();

    if (modo == 2 && gravando == false) {
      unsigned long instanteAtual2 = millis();
      if(instanteAtual2 >= instanteAnterior2 + intervalos[indiceDoEstaloAtual]){
        Serial.println(intervalos[indiceDoEstaloAtual]);
        tone(campainhaPassiva, 440, 50);
        instanteAnterior2 = instanteAtual2;
        indiceDoEstaloAtual++;
        if (indiceDoEstaloAtual > totalDeEstalos) {
          indiceDoEstaloAtual = 0;
        }
      }
    }


    Serial.println(notaAtual);

    int posicao = encoder.getPosition();
    if (posicao != posicaoAnterior && modo == 1){
      if (posicao > 35) {
        encoder.setPosition(35);
        posicao = 35;
      }
      else if (posicao < 0) {
        encoder.setPosition(0);
        posicao = 0;
      }
      notaAtual = posicao%11;
      oitavaAtual = posicao/11;
      posicaoAnterior = posicao;
      tocaNota(notaAtual, 200, oitavaAtual);
    }

    unsigned long instanteAtual2 = millis();
    if(instanteAtual2 >= instanteAnterior2 + intervalo && intervalo != 0 && modo == 2){
      tone(campainhaPassiva, 220, 200);
      instanteAnterior2 = instanteAtual2;
    }

    unsigned long instanteAtual3 = millis();
    if (indTempoAtual == 0 && modo == 3){
      tocaNota(indicesDeNotaDaMusica[indTempoAtual], intervalosEntreNotas[indTempoAtual], oitavasDaMusica[indTempoAtual]);
      indTempoAtual++;
      instanteAnterior3 = instanteAtual3;
    }
    else if(instanteAtual3 >= instanteAnterior3 + intervalosEntreNotas[indTempoAtual-1] && modo == 3 && indTempoAtual >= 1 && indTempoAtual < 16 ){
      tocaNota(indicesDeNotaDaMusica[indTempoAtual], intervalosEntreNotas[indTempoAtual], oitavasDaMusica[indTempoAtual]);
      indTempoAtual++;
      instanteAnterior3 = instanteAtual3;
    }

}

void tocaNota(int indiceNota, int duracao, int oitava) {
  if (duracao < 0) {
    tone(campainhaPassiva, frequencias[indiceNota] * pow(2, oitava));
  }
  else {
    tone(campainhaPassiva, frequencias[indiceNota] * pow(2, oitava), duracao);
  }
  char texto[20];
  sprintf(texto, "%s%d", nomeDasNotas[indiceNota], oitava);
  Serial.print(texto);
  display.set(texto);
}

void modoAfinador(GFButton& botao) {
  modo = 1;
  intervalo = 0;
  tocaNota(notaAtual, -1, oitavaAtual);
}

void paraAfinador(GFButton& botao) {
  noTone(campainhaPassiva);
}

void modoEstalo(GFButton& botao) {
  modo = 2;
  if (gravando == false){
    Serial.println("Começou a gravar");
    gravando = true;
    indiceDoEstaloAtual = 0;
    totalDeEstalos = 0;
  }
  else {
    Serial.println("Parou de gravar");
    gravando = false;
    unsigned long instanteAtual = millis();
    if(instanteAtual > instanteAnterior + 10){
      totalDeEstalos++;
      intervalos[indiceDoEstaloAtual] = instanteAtual - instanteAnterior;
      instanteAnterior = instanteAtual;
    }
    
    for (int i=0; i<totalDeEstalos; i++) {
      Serial.println(intervalos[i]);
    }
    indiceDoEstaloAtual = 0;
    instanteAnterior = -1;
  }
}

//void paraMetronomo(GFButton& botao) {
//  instanteDepois = millis();
//  intervalo = instanteDepois - instanteAtual;
//  int batidasPorMinuto = 60000 / intervalo;
//  display.set(batidasPorMinuto);
//}

void tickDoEncoder() {
 encoder.tick();
}

void tocaMusica(){
  modo = 3;
  indTempoAtual = 0;
}

void attEstalo(){
  if (modo == 2 && gravando == true) {
    if (instanteAnterior == -1) {
      instanteAnterior = millis();
    }
    else {
      unsigned long instanteAtual = millis();
      if(instanteAtual > instanteAnterior + 10){
        Serial.println("ESTALO");
        totalDeEstalos++;
        intervalos[indiceDoEstaloAtual] = instanteAtual - instanteAnterior;
        indiceDoEstaloAtual++;
        instanteAnterior = instanteAtual;
      }
    }
  }
}
