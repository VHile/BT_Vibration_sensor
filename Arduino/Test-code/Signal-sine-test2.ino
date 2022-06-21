#include <SoftwareSerial.h>
#include <math.h>
//#include <TimerOne.h>
#include <Wire.h>


SoftwareSerial BT(10, 11); //RX, TX

//long int ti;
unsigned long Time_1;
float d = 0;
unsigned long last_time;
void setup() {
  Wire.begin();
  Serial.begin(115200);
  while(!Serial) {}
  BT.begin(115200); 

}


void loop() {
//  for(float d = 0; d < 1; d+=0.01){
    if (millis()% 10==0){
    float resultado = 5*sin(2 * PI *20* d);//+ 10*sin(2 * PI * 25 * d);
//    last_time = millis();
    Time_1 = millis();
    d+=0.01;
    
    //Serial.println(resultado, 3);
    Serial.println(resultado, 3);
    BT.print(resultado, 3);
    BT.print("+");    
    BT.println(Time_1);
//    delay(1000);
   // delayMicroseconds(7000);                       // Sampling rate is 1/T -> 2000Hz
  }
}
