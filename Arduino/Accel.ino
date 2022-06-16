#include "MPU6050.h"
#include <SoftwareSerial.h>
#include "GyverFilters.h" // Kalman filter
MPU6050 mpu;

SoftwareSerial BT(10, 11); //RX, TX

GKalman testFilter_x(0.03 , 0.1);
GKalman testFilter_y(0.03 , 0.1);
GKalman testFilter_z(0.03 , 0.1);

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
  
  ax = mpu.getAccelerationX();  
  ay = mpu.getAccelerationY(); 
  az = mpu.getAccelerationZ(); 
  
  ax = constrain(ax, -32767, 32767);  
  gx = (ax) / 32767.0*8;        
  gx_f = testFilter_x.filtered(gx);
  
  ay = constrain(ay, -32767, 32767);   
  gy = (ay) / 32767.0*8;         
  gy_f = testFilter_y.filtered(gy);
  
  az = constrain(az, -32767, 32767);    
  gz = (az) / 32767.0*8;       
  gz_f = testFilter_z.filtered(gz);
  
   T = mpu.getTemperature();
   t = (float)T/340 + 36.53;
  
  BT.print(gx_f);
  BT.print("+");
  BT.print(gy_f);
  BT.print("+");
  BT.print(gz_f);
  BT.print("+");
  BT.println(t);

  Serial.print(gx_f);
  Serial.print("\t");
  Serial.print(gy_f);
  Serial.print("\t");
  Serial.print(gz_f);
  Serial.print("\t");
  Serial.println(); 
//  Serial.println(t); 
  delay(10);
}
