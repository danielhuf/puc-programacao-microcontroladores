#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>

MCUFRIEND_kbv tela;

#define BR_SHIELD true

#if BR_SHIELD
  TouchScreen touch(8, A3, A2, 9, 300);  // shield novo (Mekanus)
#else
  TouchScreen touch(6, A1, A2, 7, 300);  // shield antigo (China)
#endif

JKSButton botao;

void setup () {
    tela.begin( tela.readID() );
    tela.fillScreen(TFT_BLACK);
    
    botao.init(&tela, &touch, 120, 50, 200, 100, TFT_WHITE, TFT_CYAN, TFT_BLACK, "Botao 1");
    botao.setPressHandler(desenhaRetanguloVermelho);
    botao.setReleaseHandler(apagaRetangulo);
}

void loop () {
    botao.process();
}

void desenhaRetanguloVermelho (JKSButton &botaoPressionado) {
    tela.fillRect(50, 200, 140, 70, TF_RED);
}

void apagaRetangulo (JKSButton &botaoPressionado) {
    tela.fillRect(50, 200, 140, 70, TF_BLACK);
}
