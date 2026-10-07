#include <ESP32Servo.h>
Servo esc;
const int pin = 18;
int value = 1000;
int commande = 1000;


void setup() {
  Serial.begin(115200);
  esc.attach(pin,1000,2000);
  esc.writeMicroseconds(1000);
  delay(3000);
}

void loop() {

  if (Serial.available()>0){
    int reading = Serial.parseInt();
    if (reading==0){
        value = 1000;
      }
    else {
        value = constrain(reading,1000,2000);
    }
    Serial.println(value);
  }

  if (commande<value){
    commande+=2;
  }
  else if (commande>value){
    commande = value;
  }
  esc.writeMicroseconds(commande);
  delay(10);
}
