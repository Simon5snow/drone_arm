// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

float biais_gyro = 0;
unsigned long time_after;
unsigned long dernier_tick=0;
unsigned  long dernier_passage = 0;
float angle = 0;


void setup(void) {
  delay(2000);
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");


  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  sensors_event_t a, g, temp;


  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_94_HZ);
  Serial.print("Do not touch the mpu");

  for (int i = 0; i<1000;i++){  
    mpu.getEvent(&a, &g, &temp);
    biais_gyro += g.gyro.x;
    delay(2);
  } 
  
  biais_gyro = biais_gyro/1000;
  Serial.println("biais gyro :");
  Serial.print(biais_gyro, 6);
  float angle = atan2(a.acceleration.y, a.acceleration.z)*180/PI;;

  delay(5000);

}

int compteur = 0;

void loop() {

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;


  time_after = micros();

  if (time_after - dernier_tick>=5000){
    mpu.getEvent(&a, &g, &temp);
    float dt = 0.005;
    float angle_accel = atan2(a.acceleration.y,a.acceleration.z)*180/PI;
    angle = 0.98*(angle + (g.gyro.x - biais_gyro)*dt*180/PI) + 0.02*angle_accel;
    
    if (compteur >= 20) {
      Serial.print("brut:");
      Serial.print(angle_accel);
      Serial.print(",filtre:");
      Serial.println(angle);
      
      compteur = 0;
    }

 
    compteur +=1;
    dernier_tick = 5000 + dernier_tick;
    dernier_passage = time_after;
  }
}