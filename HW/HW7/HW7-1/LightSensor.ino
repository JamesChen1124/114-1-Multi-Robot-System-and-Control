#include <BH1750FVI.h>
BH1750FVI LightSensor;

    
void setup() {
  Serial.begin(9600);    
  LightSensor.begin();   
  LightSensor.SetAddress(Device_Address_L);
  LightSensor.SetMode(Continuous_H_resolution_Mode);
  pre_time = millis();
}

unsigned long pre_time = 0;    
int times = 1;

void loop() {
  if (millis() - pre_time >= 10000){  
    int lux = LightSensor.GetLightIntensity();    
    Serial.print("Light: ");
    Serial.print(lux);
    Serial.println(" lux");
    pre_time = millis();

    times += 1
    if times >= 11{
      return;
    }
  }
}

