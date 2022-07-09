// Neste playground 06 A, vamos começar vendo o básico do Arduino, sem usar bibliotecas externas.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// ANTES DE COMEÇARMOS, É PRECISO AJUSTAR O MODELO DO MICROCONTROLADOR NESTE EDITOR!
// VÁ EM Ferramentas > Placa: (...) >  Arduino AVR Boards > Arduino Mega ou Mega 2560.
// VOCÊ SÓ PRECISA FAZER ISTO 1 VEZ.


// Aqui no começo do código, a gente inicia as nossas variáveis globais.
int led1 = 13;
int led2 = 12;
int led3 = 11;

int input1 = A1;
int input2 = A2;

int campainha = 3;


// A função setup é executada 1 vez, no começo do programa.
// Aqui a gente geralmente chama comandos para as configurações iniciais dos dispositivos.

void setup() {
  pinMode(campainha, OUTPUT);
  
  // Vamos começar configurando os LEDs.
  // É muito importante começar definindo os pinos deles como OUTPUT (saída).
  pinMode(led1, OUTPUT);

  // Depois do pinMode OUTPUT, o Arduino envia um LOW (0V) para esse pino.
  // Os nossos LEDs estão configurados para acender com LOW, logo o LED 1 começa aceso.

  // Para mudar o estado do LED, chamamos o digitalWrite.
  // Vamos configurar o LED 2 como saída e apagá-lo em seguida com HIGH (5V).
  pinMode(led2, OUTPUT);
  digitalWrite(led2, HIGH);


  // COMPILE O PROGRAMA INDO NO MENU Skecth > Exportar Binário Compilado.
  // DEPOIS VÁ NO SIMULIDE E ABRA O ARQUIVO playground06a.simu (USE O 3º BOTÃO NA BARRA SUPERIOR, COM O TRIÂNGULO PARA CIMA).
  // EM SEGUIDA, CLIQUE NO PRIMEIRO BOTÃO VERMELHO NO TOPO PARA LIGAR O CIRCUITO.
  // OBSERVE O LED 1 ACESO E O LED 2 APAGADO.
  // DEPOIS PARE A SIMULAÇÃO CLICANDO NOVAMENTE NO BOTÃO, QUE AGORA ESTARÁ AMARELO.


  // Para lidar com um botão, podemos usar o modo INPUT no pino dele.
  // Mais adiante, na função loop, faremos um monitoramento manual dessa entrada.
  // No playground 06 B, a gente vai ver uma alternativa mais interessante.
  pinMode(input1, INPUT);



  // NO COMEÇO DO PROGRAMA, INICIE A VARIÁVEL input2 (PARA O BOTÃO 2) NO PINO A2.
  // CONFIGURE AQUI ESSE PINO input2 COMO INPUT.
  // COMPILE O PROGRAMA NOVAMENTE COM Skecth > Exportar Binário Compilado.
  // VOLTE NO SIMULIDE. SE A SIMULAÇÃO AINDA ESTIVER RODANDO, CLIQUE NO BOTÃO AMARELO PARA PARAR.
  // CLIQUE NO PRIMEIRO BOTÃO VERMELHO NO TOPO PARA LIGAR O CIRCUITO NOVAMENTE.
  // NADA VAI ACONTECER AO APERTAR O BOTÃO 2 AINDA. SÓ ESTAMOS PRATICANDO E PREPARANDO O TERRENO PARA DEPOIS.
  pinMode(input2, INPUT);
  

  // Por fim, é importante inicializar a Serial aqui na setup.
  // Como o Arduino não tem um monitor, ele precisa enviar mensagens pelo cabo USB até o computador.
  // A Serial.begin define a taxa de transmissão dessa comunicação.
  Serial.begin(9600);


  // Depois do begin, é só enviar uma mensagem com a Serial.println.
  // Se você tivesse um Arduino físico, a tela serial seria aberta clicando no botão com lupa ali no topo direito do editor.
  // No caso Arduino do Simulide, a tela serial fica no simulador.
  Serial.println("Iniciei o programa com a setup!");


  // Outro comando útil é o delay, que é equivalente ao sleep que a gente usava no Python.
  // Ele também trava a execução do programa, então temos que usar com cautela.
  // Uma diferença importante é que a delay recebe o tempo em milissegundos.
  delay(500);
  Serial.println("Passaram-se 500 milissegundos");

  

  // COMPILE O CÓDIGO AQUI, VOLTE PARA O SIMULIDE E REINICIE A SIMULAÇÃO.
  // CLIQUE COM O BOTÃO DIREITO NA PLACA AZUL DO ARDUINO E SELECIONE SERIAL MONITOR.
  // RODE A SIMULAÇÃO E VEJA AS DUAS MENSAGENS APARECENDO.
    


  // NO COMEÇO DO PROGRAMA, INICIE A VARIÁVEL DO LED 3 PARA O PINO 11.
  // CONFIGURE AQUI ESSE PINO COMO OUTPUT, O QUE FARÁ ELE ACENDER.
  // DEPOIS ESPERE 700 MILISSEGUNDOS E APAGUE O LED COM A digitalWrite.
  // OBS: O LED VAI DEMORAR UM POUQUINHO PARA ACENDER POR CAUSA DO DELAY QUE FIZEMOS ANTES.
  pinMode(led3, OUTPUT);
  delay(700);
  digitalWrite(led3, HIGH);


  // Vou imprimir uma última frase na Serial, para sinalizar o fim da setup.
  Serial.println("Terminei a setup. Agora vai iniciar o loop do programa.");
}


// Depois da setup, a função loop fica sendo chamada continuamente.
// Ela é equivalente ao "while True" lá do nosso Python.

int contagem = 0;
void loop() {
  
  // Para mostrar a repetição da função loop, vamos fazer um serial com delay.
  // Perceba que eu posso chamar print em vez de println, para gerar a frase com dois comandos.
  // A gente vai aprender mais tarde como juntar um número com uma string no Arduino.


  // DESCOMENTE AS LINHAS ABAIXO, RECOMPILE E RODE A SIMULAÇÃO PARA VER O RESULTADO.
  
  //contagem++;
  //Serial.print("Contando as repeticoes no loop: ");
  //Serial.println(contagem);
  //delay(500);


  // Dentro da loop, eu posso monitorar as entradas com a digitalRead.
  // Por exemplo, o código abaixo acende o LED 2 de acordo com a leitura do botão 1.
  // Mas o delay no loop prejudica a interatividade, por travar o programa a cada 500 ms.
  if ( digitalRead(input1) == LOW ) {
    digitalWrite(led2, LOW);
  }
  else {
    digitalWrite(led2, HIGH);
  }


  // COMPILE O CÓDIGO AQUI, VOLTE PARA O SIMULIDE E PERCEBA O ATRASO DO BOTÃO 1.
    // OBS: CLIQUE NO QUADRADO CINZA PARA PRESSIONAR O BOTÃO.
  // EM SEGUIDA, COMENTE NOVAMENTE AS 4 LINHAS INICIAS DA LOOP E VEJA A DIFERENÇA SEM O ATRASO.



  // NO COMEÇO DO PROGRAMA, CRIE UMA VARIÁVEL PARA A CAMPAINHA NO PINO 3.fi
  // CONFIGURE ESSE PINO COMO OUTPUT NA setup.
  // MONITORE AQUI EMBAIXO O ESTADO DO BOTÃO 2 COM A digitalRead:
    // SE O BOTÃO 2 ESTIVER PRESSIONADO, TOQUE A CAMPAINHA.
    // CASO CONTRÁRIO, DESLIGUE A CAMPAINHA.
  if ( digitalRead(input2) == LOW ) {
    digitalWrite(campainha, LOW);
  }
  else {
    digitalWrite(campainha, HIGH);
  }
  // OBS: O VOLUME DA CAMPAINHA É BEM ALTO!
  



}
