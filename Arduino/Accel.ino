#include "MPU6050.h"
#include <SoftwareSerial.h>
#include "GyverFilters.h"
#include <TimerOne.h>

MPU6050 mpu;

SoftwareSerial BT(10, 11); //RX, TX

GKalman testFilter_x(0.03 , 0.1);
GKalman testFilter_y(0.03 , 0.1);
GKalman testFilter_z(0.03 , 0.1);

// Initial time
long int Time_1;

int16_t ax, ay, az, T;
float gx, gy, gz, t, gx_f, gy_f, gz_f;

void setup() {
  Wire.begin();
  Serial.begin(115200);
  while(!Serial) {}
  BT.begin(115200); 
  mpu.initialize();     
  mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_8);
  mpu.setXAccelOffset(-1969);
  mpu.setYAccelOffset(-43);
  mpu.setZAccelOffset(1413);

}


void loop() {
  
  ax = mpu.getAccelerationX();  // ускорение по оси Х
  ay = mpu.getAccelerationY();  // ускорение по оси y
  az = mpu.getAccelerationZ();  // ускорение по оси Z
  Time_1 = millis();
  ax = constrain(ax, -32767, 32767);    // ограничиваем +-1g
  gx = (ax) / 32767.0*8;           // переводим в +-1.0
  gx_f = testFilter_x.filtered(gx);
  
  ay = constrain(ay, -32767, 32767);    // ограничиваем +-1g
  gy = (ay) / 32767.0*8;           // переводим в +-1.0
  gy_f = testFilter_y.filtered(gy);
  
  az = constrain(az, -32767, 32767);    // ограничиваем +-1g
  gz = (az) / 32767.0*8;           // переводим в +-1.0
  gz_f = testFilter_z.filtered(gz);
  
  T = mpu.getTemperature();
  t = (float)T/340 + 36.53;


  BT.print(gx_f);
  BT.print("+");
  BT.print(gy_f);
  BT.print("+");
  BT.print(gz_f);
  BT.print("+");
  BT.print(t);
  BT.print("+");
  BT.println(Time_1);

/*
  Serial.print(gx);
  Serial.print("\t");
  Serial.print(gy);
  Serial.print("\t");
  Serial.print(gz);
  Serial.print("\t");
*/
/*
  Serial.print(gx_f);
  Serial.print("\t");
  Serial.print(gy_f);
  Serial.print("\t");
  Serial.print(gz_f);
  Serial.print("\t");
  Serial.println();
  Serial.println(t); 
*/    
  delay(10);
}
