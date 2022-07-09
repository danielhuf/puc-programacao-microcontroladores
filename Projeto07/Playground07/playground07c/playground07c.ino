// Neste playground 06 C, vamos trabalhar com o buzzer passivo e o encoder.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


// Como de costume, a gente começa importando as bibliotecas e criando as variáveis globais.
#include <RotaryEncoder.h>
#include <GFButton.h>
#include <ShiftDisplay.h>

int campainhaPassiva = 5;
RotaryEncoder encoder(20, 21);
GFButton botao1(A1);
ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

int posicaoAnteriorDoEncoder = 0;
int frequencia = 100;
unsigned long instanteAnteriorDaContagem = 0;

void setup() {
  
  // Normalmente, a gente conectaria um dos pinos da campainha passiva direito no terra e outro numa saída.
  // Mas para aproveitar a estrutura de encaixe no shield multifunção, vamos usar dois pinos.
  // Um dele é o A5, que vai ser ajustado para ser sempre LOW, como se fosse um terra.
  pinMode(A5, OUTPUT);
  digitalWrite(A5, LOW);

  // O outro pino 5 é a nossa saída, porque ele tem a funcionalidade de PWM.
  pinMode(5, OUTPUT);


  // Para o encoder, vamos monitorar os pinos de entradas com a interrupção.
  // Isso vai garantir que detecte giros bem rápidos, sem perder posições.
  attachInterrupt(digitalPinToInterrupt(20), detectarTick, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), detectarTick, CHANGE);


  // O botão 1 segue a receita de antes.
  botao1.setPressHandler(apertouBotao1);


  // E, como sempre, vamos inicializar a serial aqui na setup também.
  Serial.begin(9600);

}


// Função chamada pela interrupção nos pinos do encoder, para que ele monitore os giros.
void detectarTick() {
  encoder.tick();
}


// Função do nosso botão 1.
void apertouBotao1(GFButton &button) {

  // Vamos tocar a campainha com 220 Hz de frenquencia, durante 300 ms.
  tone(campainhaPassiva, 220, 300);


  // COMPILE E REINICIE A SIMULAÇÃO.
  // APERTE O BOTÃO 1 PARA OUVIR A CAMPAINHA PASSIVA.
  // DEPOIS EXPERIMENTE OUTROS VALORES DE FREQUÊNCIA.
  
}


void loop() {

  // Se GFButton no código, não esquece de chamar a process.
  botao1.process();

  
  // Vamos usar o loop para obter a posição do encoder e mostrá-la no display.
  display.set(encoder.getPosition());


  // E, para o display funcionar, a gente precisa chamar a update.
  // Mas lembre que essa gasta uns 4 milissegundos para circular entre os dígitos.
  display.update();

  
  // Se eu chamasse a encoder.tick() aqui na loop, o monitoramento seria prejudicado por esse atraso de cima.

  
  // COMPILE E REINICIE A SIMULAÇÃO.
  // VEJA A CONTAGEM NO DISPLAY AO GIRAR O ENCODER PARA OS DOIS SENTIDOS.
  

  // Eu também posso ficar de olho na mudança de posição no encoder.
  // Por exemplo, vamos imprimir uma mensagem da serial ao
  if (posicaoAnteriorDoEncoder != encoder.getPosition()) {

    if (encoder.getPosition() > posicaoAnteriorDoEncoder) {
      Serial.println("Giro no sentido horario.");
    }
    else {
      Serial.println("Giro no sentido anti-horario.");
    }

    // Não esqueça de atualizar a variável global da posição anterior!
    posicaoAnteriorDoEncoder = encoder.getPosition();


    // COMPILE E REINICIE A SIMULAÇÃO.
    // ABRA A TELA SERIAL E VEJA AS MENSAGENS IMPRESSAS.



    // VERIFIQUE SE A POSIÇÃO DO ENCODER É UM MÚLTIPLO DE 10.
      // USE O % PARA CALCULAR O RESTO DA DIVISÃO.
    // SE FOR, TOQUE A CAMPAINHA COM 440 HZ DURANTE 100 MS.
    // COMPILE, RODE A SIMULAÇÃO E GIRE PARA VER O RESULTADO.

    if (posicaoAnteriorDoEncoder%10 == 0) {
      tone(campainhaPassiva, 440, 100);
    }
    
  }


  // CRIE UMA VARIÁVEL GLOBAL PARA CONTAR O TEMPO COM A millis.
  // CRIE UMA OUTRA VARIÁVEL GLOBAL PARA A FREQUÊNCIA DA CAMPAINHA, COMEÇANDO COM 100.
  // A CADA 1 SEGUNDO, ADICIONE 50 NESSA FREQUÊNCIA E TOQUE UM SOM BREVE COM ELA.
  // SE CHEGAR A 500, VOLTE PARA 100.

  unsigned long instanteAtual = millis(); 
  if (instanteAtual > instanteAnteriorDaContagem + 1000) {
    frequencia += 50;
    if (frequencia > 500) {
      frequencia = 100;
    }
    tone(campainhaPassiva, frequencia, 100);
    instanteAnteriorDaContagem = instanteAtual; 
  }
  

}
