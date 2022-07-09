// COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>

MCUFRIEND_kbv tela;
TouchScreen touch(6, A1, A2, 7, 300);
const int TS_LEFT = 145, TS_RT = 887, TS_TOP = 934, TS_BOT = 158;
JKSButton botao_dec;
JKSButton botao_pou;
JKSButton botao_esq;
JKSButton botao_fre;
JKSButton botao_dir;

void decolar(JKSButton &botao) {
  Serial.println("decolar");
}

void pousar(JKSButton &botao) {
  Serial.println("pousar");
}

void esquerda(JKSButton &botao) {
  Serial.println("esquerda");
}

void frente(JKSButton &botao) {
  Serial.println("frente");
}

void direita(JKSButton &botao) {
  Serial.println("direita");
}

void parar(JKSButton &botao) {
  Serial.println("parar");
}

void setup() {
  Serial.begin(9600);
  tela.begin( tela.readID() );
  tela.fillScreen(TFT_BLACK);

  botao_dec.init(&tela, &touch, 60, 40, 100, 50,
                 TFT_WHITE, TFT_GREEN, TFT_BLACK, "Decolar", 2);

  botao_pou.init(&tela, &touch, 180, 40, 100, 50,
                 TFT_WHITE, TFT_RED, TFT_WHITE, "Pousar", 2);

  botao_esq.init(&tela, &touch, 40, 100, 60, 50,
                 TFT_WHITE, TFT_LIGHTGREY, TFT_BLACK, "<", 2);

  botao_fre.init(&tela, &touch, 120, 100, 60, 50,
                 TFT_WHITE, TFT_LIGHTGREY, TFT_BLACK, "^", 3);

  botao_dir.init(&tela, &touch, 200, 100, 60, 50,
                 TFT_WHITE, TFT_LIGHTGREY, TFT_BLACK, ">", 2);

  botao_dec.setPressHandler(decolar);
  botao_pou.setPressHandler(pousar);
  botao_esq.setPressHandler(esquerda);
  botao_fre.setPressHandler(frente);
  botao_dir.setPressHandler(direita);

  botao_esq.setReleaseHandler(parar);
  botao_fre.setReleaseHandler(parar);
  botao_dir.setReleaseHandler(parar);

  tela.setCursor(25, 140); tela.setTextColor(TFT_WHITE);
  tela.setTextSize(1); tela.print("Objeto Laranja Detectado");

  tela.drawRect(20, 160, 202, 152, TFT_WHITE);

}

void loop() {
  botao_dec.process();
  botao_pou.process();
  botao_esq.process();
  botao_fre.process();
  botao_dir.process();

  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();

    tela.fillRect(21, 161, 200, 150, TFT_BLACK);

    if (texto.startsWith("retangulo ")){
      int x, y, comp, alt;
      x = texto.substring(10, 13).toInt();
      y = texto.substring(14, 17).toInt();
      comp = texto.substring(18, 21).toInt();
      alt = texto.substring(22).toInt();
      tela.fillRect(x+21, y+161, comp, alt, TFT_ORANGE);
    }

    
    
    Serial.println(texto);
  }
}


// DEPOIS FAÇA OS NOVOS RECURSOS
