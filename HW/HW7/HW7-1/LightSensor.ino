#include <BH1750FVI.h>
BH1750FVI LightSensor;

unsigned long pre_time = 0;    // 非負整數
int times = 1;    // 計數

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);       // set baud rate
  LightSensor.begin();      // begin light sensor
  LightSensor.SetAddress(Device_Address_L);
  LightSensor.SetMode(Continuous_H_resolution_Mode);
  pre_time = millis();
}

void loop() {
  if (millis() - pre_time >= 10000){    // 十秒迴圈
    int lux = LightSensor.GetLightIntensity();    // 得到 Lux 數值
    
    // 運用Serial給ros2python檔用ser.readline().decode()函數讀取訊息
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
