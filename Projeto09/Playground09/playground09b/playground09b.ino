// Neste playground 09 B, vamos trabalhar com string e com a leitura serial.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// Vamos começar com algumas variáveis globais.
int led1 = 13, led2 = 12, led3 = 11, led4 = 10;
int leds[] = {led1, led2, led3, led4};
int tempoNumerico;
unsigned long instanteAnteriorDaContagem = 0;


void setup() {
  // Primeiro vamos lembrar de colocar os pinos dos LEDs como OUTPUT e apagá-los.
  for (int i = 0; i < 4; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], HIGH);
  }

  
  // Agora vamos falar de serial. Tudo começa com a begin.
  // Só lembrando que esse 9600 é a taxa de transmissão em bits por segundo.
  // Caso você precise enviar muitos dados, dá para aumentar esse valor.
  Serial.begin(9600);


  // A gente já usou a Serial.println várias vezes.
  Serial.println("----");


  // Agora imagina que a gente tenha uma variável numérica qualquer.
  int numero = 42;


  // Para imprimir esse valor na serial junto com algum texto, podemos usar comandos separados.
  Serial.print("A resposta (via serial): ");
  Serial.println(numero);


  // Também vimos no Projeto 07 como usar a sprintf para juntar texto com número.
  // Essa função é de C, bem "baixo nível". Tem que lembrar do \0 e tomar cuidado para não invadir memória.
  // Outro problema é que o sprintf no Arduino não funciona bem com %f.
  char bufferGrande[100];
  sprintf(bufferGrande, "A resposta (via sprintf): %d", numero);
  Serial.println(bufferGrande);

  
  // Agora na teoria 09, vimos a biblioteca String do Arduino.
  String texto = "A resposta (via String): ";


  // Ela facilita a manipulação de texto, deixando a coisa mais parecida como Python.
  // Por exemplo, dá para converter o número para texto e concatenar com o +.
  String numeroComTexto = String(numero);
  String frase = texto + numeroComTexto;
  Serial.println(frase);


  // Você pode até especificar o número de casas decimais para floats nessa conversão.
  float numeroDecimal = 42.42;
  String frase2 = "A resposta (com mais casas decimais): " + String(numeroDecimal, 3);
  Serial.println(frase2);


  // EXPORTE O BINÁRIO COMPILADO, ABRA O MONITOR SERIAL E RODE A SIMULAÇÃO.
  // VEJA OS RESULTADOS IMPRESSOS.


  // CALCULE A RAIZ QUADRADA DE 35 USANDO A FUNÇÃO sqrt E COLOQUE O RESULTADO NUMA VARIÁVEL FLOAT.
  // COLOQUE O RESULTADO NUMA STRING COM 5 CASAS DEMAIS, NO FORMATO "Raiz quadrada de 35 = _______ (aproximadamente)."
  // IMPRIMA ESSA STRING NA SERIAL.
  float raiz = sqrt(35);
  String frase3 = "Raiz quadrada de 35 = " + String(raiz, 5) + " (aproximadamente);";
  Serial.println(frase3);

  // Dentro da loop, vamos trabalhar com a leitura na Serial.
  // O programa vai ficar travado enquanto a mensagem não chegar completamente.
  // Por isso, é bom colocar um limite na espera pelo recebimento da mensagem.
  // O tempo padrão é de 1000ms. Vou usar 10ms aqui, mas isso pode variar de caso a caso.
  Serial.setTimeout(10);
}

void loop() {
  // Obs: eu atualizei a teoria na parte da leitura serial, mas ainda não regravei o vídeo.
  // A primeira coisa a fazer é verificar se chegou alguma coisa na serial.
  // Se não tiver nada, não precisamos perder milissegundos aguardando a mensagem.
  if (Serial.available() > 0) {
    
    // Alguns tutoriais usam a Serial.read para ler byte a byte.
    // Eu prefiro ler a mensagem até encontrar um caracter de fim da frase (ex: quebra de linha).
    String textoRecebido = Serial.readStringUntil('\n');


    // Esse texto recebido pode vir com quebra de linha e/ou espaços em branco no começo e/ou no fim.
    // A função trim retira esses caracteres das extremidades da string.
    // Assim fica mais fácil analisar depois o que chegou.
    textoRecebido.trim();


    // Agora podemos usar as funções da biblioteca String para verificar o que foi recebido.
    // Por exemplo, dá para usar o ==, o que não funcionaria no char[] tradicional de C.
    if (textoRecebido == "acender") {
      digitalWrite(led1, LOW);
    }
    else if (textoRecebido == "apagar") {
      digitalWrite(led1, HIGH);
    }


    // EXPORTE O BINÁRIO, ABRA O MONITOR SERIAL E RODE A SIMULAÇÃO.
    // DIGITE "acender" e depois "apagar" NO CAMPO "Send Text:" E APERTE ENTER.
    // VEJA O LED 1 ACENDER E APAGAR.


    // Às vezes, o texto da serial pode vir com um parâmetro que queremos isolar.
    // Nesse caso, é interessante verificar se o texto começa com um trecho desejado.
    if (textoRecebido.startsWith("eu me chamo ")) {

      // Agora podemos obter o nome pegando os caracteres depois desse começo de frase.
      // Como "eu me chamo " tem 12 caracteres, vamos pegar o trecho final do texto a partir do índice 12.
      String nome = textoRecebido.substring(12);

      Serial.println("Oi, " + nome + "! Tudo bem contigo?");
    }


    // Eu também posso verificar se o texto termina com alguma coisa.
    if (textoRecebido.startsWith("eu tenho ") && textoRecebido.endsWith(" anos")) {

      // O limite da substring agora precisa de um valor final.
      // Esse segundo parâmetro é o índice do caracter **seguinte** ao final da captura.
      // Como " anos" tem 5 caracteres, vamos ir até o tamanho da string - 5.
      String idade = textoRecebido.substring(9, textoRecebido.length() - 5);


      // Se quisermos fazer alguma conta com essa idade, é preciso convertê-la para int primeiro.
      int idadeNumerica = idade.toInt();
      int decadas = idadeNumerica / 10;

      Serial.println("Voce completou " + String(decadas) + " decadas.");
    }


    // RODE A SIMULAÇÃO E INSIRA AS FRASES DE EXEMPLO ("eu me chamo ___" e "eu tenho __ anos").
    // DEPOIS VEJA O SEU NOME E A SUA IDADE IMPRESSOS NA SERIAL.


    // VERIFIQUE SE O TEXTO RECEBIDO COMEÇA COM "acender led ".
    // CASO COMECE, PEGUE O FINAL DO TEXTO (QUE SERÁ UM NÚMERO DE 1 A 4).
    // COMPARANDO ESSE NÚMERO COM 1, 2, 3 E 4, ACENDA O LED ESPECIFICADO.
    if (textoRecebido.startsWith("acender led ")) {
      String num = textoRecebido.substring(12);
      int numerico = num.toInt();
      digitalWrite(leds[numerico-1], LOW);
    }




    // VERIFIQUE SE O TEXTO RECEBIDO SEGUE O FORMATO "Apagar LED 3 daqui a ___ ms".
    // CASO COMECE, CAPTURE O PARÂMETRO (QUE PODE TER UM NÚMERO VARIÁVEL DE DÍGITOS) E CONVERTA PARA INT.
    // DEPOIS ACENDA O LED 3 E APAGUE-O APÓS PASSAR O TEMPO FORNECIDO EM MILISSEGUNDOS.
      // DICA: FAÇA UM OUTRO IF NA LOOP (FORA DO IF DA SERIAL.AVAILABLE) USANDO A millis DO PROJETO 07.
    if (textoRecebido.startsWith("Apagar LED 3 daqui a ") && textoRecebido.endsWith(" ms")) {
      String tempo = textoRecebido.substring(21, textoRecebido.length() - 3);
      Serial.println(tempo);
      tempoNumerico = tempo.toInt();
      digitalWrite(leds[2], LOW);
    }

      
    
  }


  // O IF DA MILLIS VAI VIR AQUI EMBAIXO!
  unsigned long instanteAtual = millis(); 
  if (instanteAtual > instanteAnteriorDaContagem + tempoNumerico) {
    digitalWrite(leds[2], HIGH);
    instanteAnteriorDaContagem = instanteAtual; 
  }
  
}
