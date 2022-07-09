// Neste playground 07 A, vamos trabalhar com a contagem de tempo usando a millis.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// Vamos começar incluindo as bibliotecas do projeto anterior.
#include <ShiftDisplay.h>
#include <GFButton.h>


// Depois iniciamos as variáveis globais dos componentes.
int led1 = 13;
int led2 = 12;

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
GFButton botao1(A1);
GFButton botao2(A2);


// E agora vamos criar as variáveis para contar quanto tempo se passou desde o início do programa.
// ATENÇÃO: lembre-se que essas variáveis precisam ser sempre do tipo unsigned long!
unsigned long instanteAnteriorDaContagem1 = 0;
unsigned long instanteAnteriorDaContagem2 = 0;
int contador = 0;
unsigned long instanteAnteriorDoBotao1 = 0;
unsigned long instanteAnteriorDoBotao2 = 0;


// Por fim, uma variável global para ajudar a piscar o LED.
bool led1Aceso = false;


// A função setup é executada 1 vez, no começo do programa.
// Aqui a gente geralmente chama comandos para as configurações iniciais dos dispositivos.

void setup() {
  
  // Vamos começar configurando os componentes.
  pinMode(led1, OUTPUT);
  digitalWrite(led1, HIGH); // para começar apagado

  botao1.setPressHandler(clicouNoBotao1);
  botao2.setPressHandler(clicouNoBotao2);
  
  // Não esqueça de inicializar a serial!
  Serial.begin(9600);
  
}


// Depois da setup, a função loop fica sendo chamada continuamente.

void loop() {
  
  // Aqui a gente chama as funções de controle do display e do botão.
  display.update(); // circula rapidamente entre os dígitos
  botao1.process(); // monitora as mudanças no botão
  botao2.process();


  // Conforme vimos no playground 06 A, o comando delay atrapalharia esses dois componentes.
  // Por isso, é mais interessante usar a millis para aguardar o tempo necessário.
  // Vamos começar com um exemplo que fica imprindo uma mensagem periodicamente.
  // A ideia é verificar se já se passaram 2 segundos (2000 ms) desde o último instante salvo.
  unsigned long instanteAtual = millis(); 
  if (instanteAtual > instanteAnteriorDaContagem1 + 2000) {
    Serial.println("Passaram-se mais 2 segundos");
    contador++;
    display.set(contador);
    display.update();

    // ATENÇÃO: não esqueça de atualizar a variável global da contagem 1!
    instanteAnteriorDaContagem1 = instanteAtual; 
  }


  // A gente poderia ter usado o TimerInterrupt em vez da millis no exemplo de cima.
  // Mas a vantagem da millis é que eu posso ter inúmeras contagens em paralelo.
  // Por exemplo, vamos usar a contagem 2 e uma variável global booleana para piscar o LED.
  if (instanteAtual > instanteAnteriorDaContagem2 + 1500) {
    
    if (led1Aceso == true) {
      digitalWrite(led1, HIGH);
      led1Aceso = false;
    }
    else {
      digitalWrite(led1, LOW);
      led1Aceso = true;
    }
    
    // ATENÇÃO: não esqueça de atualizar a variável global da contagem 2!
    instanteAnteriorDaContagem2 = instanteAtual; 
  }


  // COMPILE O PROGRAMA INDO NO MENU Skecth > Exportar Binário Compilado.
  // DEPOIS VÁ NO SIMULIDE, ABRA O ARQUIVO playground07a.simu E RODE A SIMULAÇÃO.
  // CLIQUE COM O BOTÃO DIREITO NA PLACA AZUL E ABRA O MONITOR SERIAL.
  // OBSERVE A VELOCIDADE DAS MENSAGENS IMPRESSAS E DO LED PISCANDO.
  // DEPOIS DISSO, DIMINUA O TEMPO LIMITE DAS DUAS CONTAGENS.
  // RECOMPILE, REINICIE A SIMULAÇÃO E VEJA A DIFERENÇA NO RESULTADO.
  

  // CRIE UMA NOVA VARIÁVEL DE CONTAGEM DE TEMPO NO COMEÇO DO CÓDIGO
  // USE ESSA VARIÁVEL PARA IR ADICIONANDO 1 NUMA VARIÁVEL GLOBAL.
  // MOSTRE ESSA VARIÁVEL NO DISPLAY DE 7 SEGMENTOS.
  
}


// Eu também posso fazer uma contagem de tempo fora do loop.
// Por exemplo, dá para verificar se o botão 1 está sendo pressionado várias vezes seguidas ou não.

void clicouNoBotao1 (GFButton &button) {
  unsigned long instanteAtual = millis(); 

  if (instanteAtual > instanteAnteriorDoBotao1 + 500) {
    Serial.println("Voce apertou o botao 1 com calma, muito bem.");
  }
  else {
    Serial.println("Calma, cara, vai devagar nesse botao!");
  }

  instanteAnteriorDoBotao1 = instanteAtual;


  // COMPILE, REINICIE A SIMULAÇÃO E VEJA O RESULTADO NO CLIQUE DO BOTÃO 1 NA SERIAL.
  
}

// PROGRAME PARA QUE O CLIQUE NO BOTÃO 2 ALTERE O ESTADO DO LED 1
  // MAS SE O USUÁRIO FICAR CLICANDO VÁRIAS VEZES RAPIDAMENTE, NÃO FAÇA NADA.
// ATENÇÃO: NÃO ESQUEÇA DE CHAMAR A .process() NO LOOP!
void clicouNoBotao2 (GFButton &button) {
  unsigned long instanteAtual = millis(); 

  if (instanteAtual > instanteAnteriorDoBotao2 + 500) {
    if (led1Aceso == true) {
      digitalWrite(led1, HIGH);
      led1Aceso = false;
    }
    else {
      digitalWrite(led1, LOW);
      led1Aceso = true;
    }
  }

  instanteAnteriorDoBotao2 = instanteAtual;
  
}
