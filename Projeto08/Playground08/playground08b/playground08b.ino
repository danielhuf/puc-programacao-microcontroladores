// Neste playground 08 B, vamos trabalhar com os servos e o braço mecânico.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// ATENÇÃO: O BRAÇO MECÂNICO SERÁ SIMULADO GRAFICAMENTE COM UM OUTRO COMPONENTE DO SIMULIDE.
// POR ISSO, VAMOS USAR UMA BIBLIOTECA MODIFICADA DA MEARM.

// COPIE AS PASTAS DO DIRETÓRIO bibliotecasExtras PARA A SUA PASTA Documentos/Arduino/libraries


// Depois dessa cópia, podemos importar as bibliotecas normalmente.
#include <Servo.h>
#include <meArm.h>
#include <GFButton.h>


// Vamos começar criando as variáveis dos botões.
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);


// Agora vamos para os servos.
// Cada servo vai ter a sua variável global.
// Mas, ao contrário de componentes como botões e display, não definimos os pinos aqui.
// Essa configuração vai ser feita depois na setup.
Servo servo1;
Servo servo2;

// Depois vamos iniciar o braço mecânico.
// Esses parâmetros de calibragem são referentes aos braços do laboratório.
// Na simulação, eles não interferem tanto.
meArm braco(180, 0, -pi/2, pi/2,
      135, 45, pi/4, 3*pi/4,
      180, 90, 0, -pi/2,
      30, 0, pi/2, 0);


// Na vida real, teríamos os pinos dos servos do braço conectados no Arduino.
// Na simulação, usaremos apenas um display para conectar.
// Ainda assim, vou fingir que usaremos os mesmos pinos que no laboratório.
int base = 12, ombro = 11, cotovelo = 10, garra = 9;
int posAtual = 1;
unsigned long instanteAnteriorDaContagem = 0;

void setup() {
  // É sempre bom inicializar a Serial, se precisar debugar alguma coisa.
  Serial.begin(9600);


  // Agora sim colocamos em qual pino o servo está conectado.
  // ATENÇÃO: Perceba que eu passei dois parâmetros extra no final, que não estavam na teoria.
  // O servo do SimulIDE usa comprimentos de pulso diferentes do laboratório.
  // Por isso, precisamos especificar esses valores (em milissegundos) na attach.
  servo1.attach(4, 1000, 2000);
  servo2.attach(5, 1000, 2000);
  

  // Vamos mexer esse servo usando o botão 1.
  botao1.setPressHandler(moverServo);


  // O braço mecânico também precisa da configuração de pinos aqui na setup.
  // Aliás, espero que você tenha copiado a biblioteca do meArm, como pedi no começo deste arquivo.
  braco.begin(base, ombro, cotovelo, garra);


  // Vamos mexer o braço e controlar a garra com os botões 2 e 3.
  botao2.setPressHandler(moverRapidoEFecharGarra);
  botao3.setPressHandler(moverSuaveEAbrirGarra);
}


void moverServo (GFButton &botao) {
  // Não cheguei a comentar essa função na teoria, que pega o ângulo atual do servo.
  int anguloAtual1 = servo1.read();


  // Cada vez que o botão 1 for pressionado, vamos alternar o ângulo entre 45 e 135 graus.
  if (anguloAtual1 == 45) {
    servo1.write(135);
  }
  else {
    servo1.write(45);
  }


  // COMPILE O CÓDIGO, RODE A SIMULAÇÃO E APERTE O BOTÃO 1 ALGUMAS VEZES.


  // CRIE UMA NOVA VARIÁVEL GLOBAL PARA O SERVO 2.
  // NA SETUP, DÊ UM ATTACH NELE NO PINO 5, COM OS MESMOS PARÂMETROS EXTRAS 1000 E 2000.
  // AQUI, AO APERTAR O BOTÃO 1, ADICIONE 10 NO ÂNGULO DESSE SERVO.
  // QUANDO O ÂNGULO FOR MAIOR OU IGUAL A 180, VOLTE PARA ZERO.
  int anguloAtual2 = servo2.read();
  anguloAtual2 += 10;
  if (anguloAtual2 >= 180) {
    anguloAtual2 = 0;
  }
  servo2.write(anguloAtual2);

}


void moverRapidoEFecharGarra (GFButton &botao) {
  // Eu posso mover a garra instantaneamente para uma posição (X, Y, Z).
  // No simulador, a altura do braço será representada por uma barra vertical no display.
  braco.goDirectlyTo(-100, 180, 50);


  // Também posso fechar a garra.
  braco.closeGripper();
}


void moverSuaveEAbrirGarra (GFButton &botao) {
  // Já a gotoPoint move o braço suavemente para uma posição (X, Y, Z).
  braco.gotoPoint(70, 100, 0);


  // Também posso abrir a garra.
  braco.openGripper();


  // COMPILE O CÓDIGO, RODE A SIMULAÇÃO E APERTE Os BOTÕES 2 E 3 ALGUMAS VEZES.
  // VEJA A DIFERENÇA NO MOVIMENTO DO BRAÇO.
}


void loop() {
  // Não esqueça de chamar a process dos botões!
  botao1.process();
  botao2.process();
  botao3.process();


  // AGORA VAMOS MOVER A GARRA CICLICAMENTE ENTRE 3 POSIÇÕES DE SUA ESCOLHA.
  // USE A MILLIS DO PROJETO PASSADO PARA EXECUTAR COMANDOS A CADA 1000 MILISSEGUNDOS.
  // DENTRO DO IF DA MILLIS AQUI EMBAIXO, MOVA A GARRA INSTANTANEAMENTE A PRÓXIMA POSIÇÃO.
    // DICA: USE UMA OUTRA VARIÁVEL GLOBAL PARA CONTAR QUAL A POSIÇÃO ATUAL (EX: 0→1→2→0→1→2→ETC)
    // DICA: VOCÊ PODE USAR VETORES PARA X, Y E Z, SE QUISER.
  unsigned long instanteAtual = millis(); 
  if (instanteAtual > instanteAnteriorDaContagem + 1000) {
    if (posAtual == 1) {
      braco.goDirectlyTo(0, 0, 0);
      posAtual++;
    }
    else if (posAtual == 2) {
      braco.goDirectlyTo(100, 100, 100);
      posAtual++;
    }
    else {
      braco.goDirectlyTo(-100, -100, -100);
      posAtual = 1;
    }
    instanteAnteriorDaContagem = instanteAtual; 
  }
}
