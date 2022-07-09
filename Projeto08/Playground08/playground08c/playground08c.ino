// Neste playground 08 C, vamos trabalhar com o armazenamento de dados na EEPROM.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// Como sempre, a gente começa importando as bibliotecas e criando as variáveis globais.
#include <EEPROM.h>
#include <GFButton.h>

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);
GFButton botao4(A4);
GFButton botao5(A5);


// Essas duas variáveis abaixo estão sem valores iniciais de propósito.
// Elas serão ajustadas pela EEPROM e pelos botões.
int ultimoBotaoApertado;
int listaDeNumeros[10];
int multiplicador = 1;


// Vamos começar com as funções que salvam na EEPROM qual foi o último botão pressionado.
// Escolhi o endereço 0 da memória neste caso.
void apertouBotao1 (GFButton &botao) {
  ultimoBotaoApertado = 1;
  EEPROM.put(0, ultimoBotaoApertado);

  Serial.println("Salvei o botao 1!");
}


void apertouBotao2 (GFButton &botao) {
  ultimoBotaoApertado = 2;
  EEPROM.put(0, ultimoBotaoApertado);

  Serial.println("Salvei o botao 2!");
}


void apertouBotao3 (GFButton &botao) {
  ultimoBotaoApertado = 3;
  EEPROM.put(0, ultimoBotaoApertado);

  Serial.println("Salvei o botao 3!");

  // No caso do botão 3, vou salvar também uma lista de números na memória.
  int valoresParaSalvar[10] = {67, 17, 53, 90, 79, 21, 64, 83, 69, 42};

  // Como já salvamos um número inteiro (2 bytes) no endereço 0, vou usar o endereço 2 desta vez.
  // Perceba que eu não preciso fazer um for para salvar cada valor individualmente.
  // A EEPROM.put já é esperta e salva todo o bloco de memória de uma vez.
  EEPROM.put(2, valoresParaSalvar);

  Serial.println("Salvei novos valores na lista!");
}

void apertouBotao4 (GFButton &botao) {
  multiplicador *= 2;
  EEPROM.put(25, multiplicador);
  Serial.println("Salvei o multiplicador!");
}

void apertouBotao5 (GFButton &botao) {
  EEPROM.get(2, listaDeNumeros);
  for (int i = 0; i < 10; i++) {
    listaDeNumeros[i] += 10;
  }
  EEPROM.put(2, listaDeNumeros);
  Serial.println("Salvei novos valores na lista!");
}


void setup() {
  // Na setup, começamos com inicialização da Serial.
  Serial.begin(9600);
  Serial.println("");


  // Depois associamos às funções anteriores aos botões
  botao1.setPressHandler(apertouBotao1);
  botao2.setPressHandler(apertouBotao2);
  botao3.setPressHandler(apertouBotao3);
  botao4.setPressHandler(apertouBotao4);
  botao5.setPressHandler(apertouBotao5);

  
  // A setup é um ótimo lugar para carregar dados salvos na EEPROM, logo que o programa começa.
  // Começamos com o mesmo endereço 0 onde salvamos.
  EEPROM.get(0, ultimoBotaoApertado);
  
 
  // Dependendo do valor carregado, vamos imprimir qual foi o último botão pressionado.
  // Lembre-se EEPROM pode estar "vazia", sem nenhum dado salvo ainda.
  if (ultimoBotaoApertado >= 1 && ultimoBotaoApertado <= 3) {
    Serial.print("Ultimo botao pressionado anteriomente: ");
    Serial.println(ultimoBotaoApertado);
  }
  else {
    Serial.println("Nenhum dado salvo ainda sobre o ultimo botao pressionado");
  }


  // COMPILE O CÓDIGO, ABRA O ARQUIVO DA SIMULAÇÃO E ABRA A TELA SERIAL.
  // RODE A SIMULAÇÃO E VEJA A MENSAGEM NA SERIAL.
  // EM SEGUIDA, TESTE O REGISTRO DE DADOS COM OS BOTÕES 1 E 2 (DEIXE O 3 PARA MAIS TARDE).
  // AGORA PARE A SIMULAÇÃO, RODE NOVAMENTE E VEJA A NOVA MENSAGEM INICIAL NA SERIAL.


  // CRIE UMA VARIÁVEL GLOBAL PARA O BOTÃO 4 (PORTA A4) E PARA UM INTEIRO COMEÇANDO EM 1.
  // AO APERTAR O BOTÃO 4, MULTIPLIQUE O INTEIRO POR 2 E SALVE NO ENDEREÇO 25 DA EEPROM.
  // POR FIM, AQUI NA SETUP, CARREGUE E IMPRIMA O VALOR SALVO NESSE ENDEREÇO.
  // APERTE O BOTÃO REINICIANDO A SIMULAÇÃO ALGUMAS VEZES PARA VER O RESULTADO.
  EEPROM.get(25, multiplicador);
  if (multiplicador < 0) {
    multiplicador = 1;
  }
  Serial.print("Ultimo valor do multiplicador: ");
  Serial.println(multiplicador);


  // Para carregar a lista salva no endereço 2, basta usar a get.
  // Assim como na put, eu não preciso fazer um for.
  // A get já carrega todos os valores, dado que a variável da lista tem um tamanho fixo conhecido.
  EEPROM.get(2, listaDeNumeros);


  // DESCOMENTE AS LINHAS ABAIXO, COMPILE O CÓDIGO E VEJA OS VALORES IMPRESSOS SERIAL.
  // DEPOIS APERTE O BOTÃO 3, REINICIE A SIMULAÇÃO E VEJA OS NOVOS VALORES IMPRESSOS.

  Serial.print("Valores no endereco 2: ");
  for (int i = 0; i < 10; i++) {
    Serial.print(listaDeNumeros[i]);
    if (i < 9) {
      Serial.print(", "); 
    }
  }
  Serial.println("");


  // AO APERTAR O BOTÃO 5 (PORTA A5), PERCORRA A listaDeNumeros, ADICIONE 10 NOS ELEMENTOS E SALVE A LISTA.
  // REINICIE A SIMULAÇÃO ALGUMAS VEZES DEPOIS DE APERTAR O BOTÃO 5.
  // VEJA OS VALORES SE ATUALIZANDO NA SERIAL.


  // AGORA BRINQUE À VONTADE, JUNTANDO A EEPROM COM OUTROS COMPONENTES!
  // SUGESTÃO: USE A EEPROM PARA RESTAURAR A POSIÇÃO ANTERIOR DO ENCODER.
    // 1. RELEMBRE A RECEITA DO ENCODER COM A attachInterrupt E A millis
    // 2. EXIBA A POSIÇÃO DO ENCODER NO DISPLAY (DENTRO DA loop)
    // 3. CASO A POSIÇÃO DO ENCODER MUDE, SALVE-A NUM OUTRO ENDEREÇO DA EEPROM.
    // 4. USE A get E A setPosition PARA RESTAURAR A POSIÇÃO ANTERIOR QUANDO O PROGRAMA COMEÇAR.
      // DICA: CRIE UMA VARIÁVEL TIPO long PARA CARREGAR DA MEMÓRIA.
  
}


void loop() {
  // Não esqueça de chamar a process dos botões!
  botao1.process();
  botao2.process();
  botao3.process();
  botao4.process();
  botao5.process();


}
