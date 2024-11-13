#include <Servo.h>
Servo dedao;
Servo indicador;
Servo medio;
Servo anelar;
Servo mindinho;

String comando;

int posicoes_atuais[5] = {90, 180, 90, 180, 90};

void setup() {
 // Inicia a comunicação serial
  Serial.begin(9600);
  dedao.attach(5);
  indicador.attach(6);
  medio.attach(9);
  anelar.attach(10);
  mindinho.attach(11);
  
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    comando = Serial.readStringUntil('\n'); 
    int posicoes_novas[5] = {0, 0, 0, 0, 0}; 
    
    //atualiza as posições
    for (int i = 1; i <= 5; i++) {
      int index = comando.indexOf("d" + String(i) + ":");
      if (index != -1) {
        int comeco = index + 3;
        int final = comando.indexOf(";", comeco);
        if (final != -1) {
          posicoes_novas[i - 1] = comando.substring(comeco, final).toInt();
        }
      }
    }

    // Ve se algum dedo foi movido
    bool dedoMovido = false;
    for (int i = 0; i < 5; i++) {
      if (posicoes_novas[i] != posicoes_atuais[i]) {
        posicoes_atuais[i] = posicoes_novas[i];
        dedoMovido = true; 
      }
    }

    // Move os servos de acordo com as novas posições
    dedao.write(posicoes_atuais[0]);
    indicador.write(posicoes_atuais[1]);
    medio.write(posicoes_atuais[2]);
    anelar.write(posicoes_atuais[3]);
    mindinho.write(posicoes_atuais[4]);

    //se algum dedo for movido, vai acender o led da placa
    if (dedoMovido) {
      digitalWrite(13, HIGH); 
      delay(500);             
      digitalWrite(13, LOW);  
      delay(500);
    }
  }
}
