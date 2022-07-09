// Neste playground 07 B, vamos trabalhar com o conceito de interrupção e com o sensor de som.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// Vamos inicializar os alguns pinos de entrada e saída, sem usar bibliotecas.
int led1 = 13;
int led2 = 12;
int sensorDeSom = 19;

int entrada1 = A1;
int entrada2 = 20;


unsigned long instanteAnteriorDoSom = 0;


void setup() {
  // Agora a gente configura na setup os pinos como entrada ou saída.
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(entrada1, INPUT);
  pinMode(entrada2, INPUT);


  // E nãoo esqueça de colocar HIGH nos LEDs, para eles começarem apagados
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);


  // Agora vamos configurar uma interrupção para a entrada 2.
  // Assim que alguma mudança acontecer nessa porta, chamaremos uma determinada função nossa.
  int origem = digitalPinToInterrupt(entrada2);
  attachInterrupt(origem, mudouAlgoNaEntrada2, CHANGE); 


  // E vamos configurar uma outra interrupção para o pino do sensor de som.
  // Neste caso, vou optar por só detectar a subida de tensão.
  int origem2 = digitalPinToInterrupt(sensorDeSom);
  attachInterrupt(origem2, detectouSom, RISING); 


  // Só lembrando que, por padrão, só alguns pinos do Arduino Mega (2, 3, 18, 19, 20 e 21) estão configurados para interrupção.
  // Se quiser usar outros pinos no futuro, pesquise sobre o PCINT.


  // Por fim, não esqueça de inicializar a serial!
  Serial.begin(9600);
}


// Para testar o poder da interrupção, vamos dar um delay bem grande na loop.
// Isso travaria o programa, mas a interrupção vai pausar a execução principal para rodar a função.
// A gente fez um teste bem parecido no Playground 06C com a TimerInterrupt, lembra?
// Ela fazia uma interrupção similar, mas de acordo com o tempo. Aqui vai ser de acordo com uma entrada.

void loop() {
  // Bloqueio com um delay bem grande.
  Serial.println("Vou bloquear a loop por mais 3 segundos.");
  delay(3000);
  Serial.println("Fim do bloqueio na loop.");


  // Veja que o monitoramento da entrada 1 aqui seria bem prejudicado.
  // Você precisaria segurá-lo por um bom tempo para ver o resultado.
  if (digitalRead(entrada1) == LOW) {
    digitalWrite(led1, LOW);
  }
  else {
    digitalWrite(led1, HIGH);
  }
}


// A gente configurou esta função aqui para a interrupção na entrada 2.
// Ou seja, assim que houver uma mudança lá, a função será chamada imediatamente, ignorando o delay.
void mudouAlgoNaEntrada2() {
  if (digitalRead(entrada2) == LOW) {
    digitalWrite(led2, LOW);
  }
  else {
    digitalWrite(led2, HIGH);
  }
}


// O sensor de som também usa uma interrupção, pois o estalo dura muito pouco tempo.
// Só que, por causa do bounce, esta função pode ser chamada várias vezes a cada estalo.
// Por isso, a gente precisa usar a contagem de tempo que vimos no Playground 07 A.
// Obs: o tempo do debounce está maior que na teoria por uma limitação do simulador.
  // Aliás, a detecção de som aqui é representada por um clique no botão dentro do sensor.
void detectouSom () {
    Serial.println("Mudanca detectada na entrada do sensor!");
  
    unsigned long instanteAtual = millis();
    if (instanteAtual > instanteAnteriorDoSom + 200) {
        Serial.println(" *** Deteccao sem bounce. ***");
        instanteAnteriorDoSom = instanteAtual;
    }
}


// COMPILE, ABRA O SERIAL E REINICIE A SIMULAÇÃO.
// TESTE A DEMORA NO BOTÃO 1 (SEGURE POR UM TEMPO) E A RAPIDEZ NO BOTÃO 2.
// CLIQUE RAPIDAMENTE NO BOTÃO DO SENSOR DE SOM E VEJA O EFEITO DO DEBOUNCE NA SERIAL.
  // TALVEZ SEJA NECESSÁRIO MEXER NO TEMPO DENTRO DO IF, DEPENDENDO DO SEU CASO.
