// Neste playground 09 A, vamos trabalhar com o motor DC e com o sensor ótico.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// Como sempre, a gente começa importando as bibliotecas e criando as variáveis globais.
#include <ShiftDisplay.h>
#include <GFButton.h>
#include <AFMotor.h>

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

int sensorOtico1 = A11;
int sensorOtico2 = A12;

bool frente = true;
int vel = 50;

unsigned long instanteAnteriorDaContagem = 0;


// O shield da Adafruit vem com 4 pontos de conexões para motores DC.
// Na hora de instanciar o motor, passamos o número desse ponto de conexão.
// Ou seja, esse número 3 não é a porta digital 3 do Arduino!
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void setup() {
  // Como sempre, é bom iniciar logo a serial.
  Serial.begin(9600);


  // Vamos começar girando o motor 3 com o comando run.
  // Ele uma das 3 direções: FORWARD (frente), BACKWARD (trás) ou RELEASE (parado).
  motor3.run(FORWARD);
  motor4.run(FORWARD);


  // Por padrão, o motor gira com a velocidade máxima.
  // O comando setSpeed muda essa velocidade, recebendo algo entre 0 e 255.
  motor3.setSpeed(150);
  motor4.setSpeed(50);


  // EXPORTE O BINÁRIO COMPILADO, RODE A SIMULAÇÃO E VEJA O MOTOR GIRANDO.
  // DEPOIS EXPERIMENTE OUTRAS VELOCIDADES E OUTRAS DIREÇÕES.


  // CRIE UMA NOVA VARIÁVEL GLOBAL PARA O MOTOR 4.
  // COMECE GIRANDO O MOTOR 4 AQUI NA SETUP PARA A FRENTE, COM VELOCIDADE 50.
  // CADA VEZ QUE APERTAR O BOTÃO 1, ALTERNE A DIREÇÃO DO MOTOR ENTRE FRENTE E TRÁS.
    // DICA: USE UMA VARIÁVEL GLOBAL BOOLEANA.
  botao1.setPressHandler(alteraDirecao);


  
  // CRIE UMA VARIÁVEL GLOBAL PARA A VELOCIDADE COMEÇANDO COM 50.
  // AO APERTAR O BOTÃO 2, ADICIONE 50 NESSA VELOCIDADE. SE PASSAR DE 250, VOLTE PARA 50.
  // AJUSTE A VELOCIDADE DO MOTOR PARA ESSA VELOCIDADE.
  botao2.setPressHandler(alteraVelocidade);

}

void loop() {
  // Não esqueça de chamar o process dos botões!
  botao1.process();
  botao2.process();
  botao3.process();


  // O sensor ótico não tem muito mistério.
  // No SimulIDE, eu tive que representá-lo por um potenciômetro.
  // Você pode fazer a leitura analógica dele, como vimos no Projeto 08.
  int nivelDeEscuridao = analogRead(sensorOtico1);


  // Também posso fazer a leitura digital do sensor.
  int estaEscuro = digitalRead(sensorOtico1);


  // IMPRIMA ESSES DOIS VALORES LIDOS A CADA 1000 MS USANDO A MILLIS.
  unsigned long instanteAtual = millis(); 
  if (instanteAtual > instanteAnteriorDaContagem + 1000) {
    Serial.println(nivelDeEscuridao);
    Serial.println(estaEscuro);
    instanteAnteriorDaContagem = instanteAtual; 
  }

}

void alteraDirecao(GFButton &botao) {
  if (frente)
    motor4.run(BACKWARD);
  else
    motor4.run(FORWARD);
  frente = !frente;
}

void alteraVelocidade(GFButton &botao) {
  vel += 50;
  if (vel > 250)
    vel = 50;
  motor4.setSpeed(vel);
  Serial.println("oi");
}
