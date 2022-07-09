// Neste playground 06 C, vamos trabalhar com biliotecas do Timer.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// A biblioteca TimerOne que eu mencionei na teoria não funciona no simulador, infelizmente.
// Mas temos uma outra que segue a mesma ideia, só com alguns pequenos detalhes a mais.
// Por exemplo, precisamos de um define antes do include.
#define USE_TIMER_1 true
#include <TimerInterrupt.h>

int led1 = 13;
bool aceso = true; //LED começa aceso

void setup() {
  
  // A inicialização do timer define o tempo entre cada repetição e a função a ser chamada.
  // Mas veja que as chamadas mudam um pouco em relação à TimerOne da teoria.
  // ATENÇÃO: o tempo aqui é em milissegundos!
  pinMode(led1, OUTPUT);
  
  ITimer1.init();
  ITimer1.attachInterruptInterval(500, repetirMensagem);


  // Para usarmos a Serial, não esqueça da begin aqui na setup!
  Serial.begin(9600);
}


// Na função do timer, vamos imprimir uma mensagem cada vez que passar o tempo.

void repetirMensagem() {
  Serial.println("Passou +1 segundo no timer, ignorando o atraso grande na loop.");

  if (aceso) {
    digitalWrite(led1, HIGH);
    aceso = false;
  }
  else {
    digitalWrite(led1, LOW);
    aceso = true;
  }
}


// Só para testar o poder do timer, vamos dar um delay bem grande na loop.
// Isso travaria o programa, mas o timer interrompe a execução principal cada vez que o tempo acaba.

void loop() {
  Serial.println("Vou bloquear a loop por mais 6 segundos.");
  delay(6000);
  Serial.println("Fim do bloqueio na loop.");
}


// EXPORTE O BINÁRIO COMPILADO.
// VÁ NO SIMULIDE E ABRA O ARQUIVO playground06c.simu.
// CLIQUE COM O BOTÃO DIREITO NA PLACA AZUL DO ARDUINO E SELECIONE SERIAL MONITOR.
// RODE A SIMULAÇÃO E VEJA O RESULTADO DO TIMER.



// MUDE O TEMPO DO TIMER PARA 500 MILISSEGUNDOS.
// CONFIGURE O LED 1 (PINO 13) COMO SAÍDA.
// ADICIONE MAIS COMANDOS NA FUNÇÃO repetirMensagem PARA MUDAR O ESTADO DESSE LED ENTRE ACESO E APAGADO.
// COMPILE, REINICIE A SIMULAÇÃO E VEJA O LED PISCANDO.
// DICA: USE UMA VARIÁVEL TIPO bool (true/false) PARA SABER SE É PARA ACENDER OU APAGAR.
