#include <Servo.h>

Servo dedao;
Servo indicador;
Servo medio;
Servo anelar;
Servo mindinho;

bool teste = true;
  
void setup() {
  dedao.attach(5);
  indicador.attach(6);
  medio.attach(9);
  anelar.attach(10);
  mindinho.attach(11);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
}

void loop() {
  while(teste ==true){
  
  
    dedao.write(180);
    delay(2000);
    dedao.write(0);
    delay(2000);

    indicador.write(180);
    delay(2000);
    indicador.write(0);
    delay(2000);

    medio.write(180);
    delay(2000);
    medio.write(0);
    delay(2000);

    anelar.write(180);
    delay(2000);
    anelar.write(0);
    delay(2000);

    mindinho.write(180);
    delay(2000);
    mindinho.write(0);
    delay(2000);

    if (dedao.read() != 0 || indicador.read() != 0 || medio.read() != 0 || anelar.read() != 0 || mindinho.read() != 0) {
      digitalWrite(8, HIGH);    
      delay(2000);
      digitalWrite(8, LOW);
      teste = false;
    } else {
      digitalWrite(7, HIGH);
      delay(2000);
      digitalWrite(7, LOW);  
      teste = false;
    }
  }
 }