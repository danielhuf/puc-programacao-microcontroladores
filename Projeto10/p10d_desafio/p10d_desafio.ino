// COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
// DEPOIS FAÇA OS NOVOS RECURSOS

// COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>
#include <LinkedList.h>

struct Ponto {
  int x;
  int y;
};

int xi, yi;

LinkedList<Ponto> listaDePontos;

bool des_pol = false;

MCUFRIEND_kbv tela;
TouchScreen touch(6, A1, A2, 7, 300);
const int TS_LEFT = 145, TS_RT = 887, TS_TOP = 934, TS_BOT = 158;
JKSButton botao_dec;
JKSButton botao_pou;
JKSButton botao_esq;
JKSButton botao_fre;
JKSButton botao_dir;

unsigned long instanteAnterior = 0;

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

  if (Serial.available() > 0 && !des_pol) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();

    tela.fillRect(21, 161, 200, 150, TFT_BLACK);

    if (texto.startsWith("retangulo ")) {
      int x, y, comp, alt;
      x = texto.substring(10, 13).toInt();
      y = texto.substring(14, 17).toInt();
      comp = texto.substring(18, 21).toInt();
      alt = texto.substring(22).toInt();
      tela.fillRect(x + 21, y + 161, comp, alt, TFT_ORANGE);
    }

    Serial.println(texto);
  }

  TSPoint ponto = touch.getPoint();
  pinMode(A1, OUTPUT); digitalWrite(A1, HIGH); // reconfigura pinos
  pinMode(A2, OUTPUT); digitalWrite(A2, HIGH); // para desenho
  int forca = ponto.z; // força aplicada na tela
  if (forca > 200 && forca < 1000) {
    if (millis() - instanteAnterior > 300) {
      int x = map(ponto.x, TS_LEFT, TS_RT, 0, 240);
      int y = map(ponto.y, TS_TOP, TS_BOT, 0, 320);

      if (x > 20 && x < 221 && y > 160 && y < 311) {
        if(!des_pol){
          tela.fillRect(21, 161, 200, 150, TFT_BLACK);
        }
        des_pol = true;
        int tamLista = listaDePontos.size();
        Ponto p;
        p.x = x - 21;
        p.y = y - 161;
        if (tamLista == 0) {
          listaDePontos.add(p);
          tela.fillCircle(x, y, 6, TFT_BLUE);

          //xi = x-21;
          //yi = y-161;
        }
        else {
          int x1, y1;
          if (p.x < listaDePontos.get(0).x + 10 && p.x > listaDePontos.get(0).x - 10
              && p.y < listaDePontos.get(0).y + 10 && p.y > listaDePontos.get(0).y - 10) {
            x1 = listaDePontos.get(0).x;
            y1 = listaDePontos.get(0).y;
            //tela.drawLine(x1 + 21, y1 + 161, x, y, TFT_BLUE);
            //Serial.println("entrei");
            //x1 = xi;
            //y1 = yi;

            x = listaDePontos.get(tamLista - 1).x + 21;
            y = listaDePontos.get(tamLista - 1).y + 161;

            String trajeto = "trajeto";
            for (int i = 0; i < tamLista; i++) {
              trajeto = trajeto + " " + String(listaDePontos.get(i).x) + " " + String(listaDePontos.get(i).y);
            }
            
            Serial.println(trajeto);
            des_pol = false;
            listaDePontos.clear();
          }
          else {
            x1 = listaDePontos.get(tamLista - 1).x;
            y1 = listaDePontos.get(tamLista - 1).y;
            listaDePontos.add(p);
            tela.fillCircle(x, y, 6, TFT_BLUE);
            //tela.drawLine(x1 + 21, y1 + 161, x, y, TFT_BLUE);
          }
          tela.drawLine(x1 + 21, y1 + 161, x, y, TFT_BLUE);
        }
      }
      //Serial.println(x + String(",") + y);
    }
    instanteAnterior = millis();
  }
}
