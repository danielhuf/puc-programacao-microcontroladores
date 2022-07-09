#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>

MCUFRIEND_kbv tela;
TouchScreen touch(6, A1, A2, 7, 300);
const int TS_LEFT = 145, TS_RT = 887, TS_TOP = 934, TS_BOT = 158;
JKSButton botao;
int r = 5;
int contagem = 0;
int x_bot = 60;
int y_bot = 270;
int comp_bot = 80;
int alt_bot = 40;

void setup() {
  Serial.begin(9600);
  tela.begin( tela.readID() );
  tela.fillScreen(TFT_BLACK);
  tela.fillRect(80, 20, 80, 20, TFT_WHITE);
  tela.fillRect(80, 40, 80, 20, TFT_RED);
  tela.fillTriangle(80, 20, 100, 40, 80, 60, TFT_BLUE);
  for (int i = 0; i < 10; i++) {
    tela.drawCircle(120, 160, r + i * 5, TFT_WHITE);
  }
  aumentaContagem();
  botao.init(&tela, &touch, x_bot, y_bot, comp_bot, alt_bot, TFT_WHITE, TFT_BLUE, TFT_WHITE, "Contar", 2);
  botao.setPressHandler(aumentaContagem);
}

void loop() {
  botao.process();
}

void aumentaContagem() {
  tela.fillRect(150, 240, 220, 300, TFT_BLACK);
  tela.setCursor(160, 250);
  tela.setTextColor(TFT_WHITE);
  tela.setTextSize(4);
  tela.print(String(contagem++));
}
