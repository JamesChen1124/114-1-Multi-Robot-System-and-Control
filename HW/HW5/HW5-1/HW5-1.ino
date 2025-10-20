#include "DHT.h"

DHT dht(2, DHT11);          // DHT11 接在 pin 2
float t = 0.0;              // 用來存放溫度
unsigned long pre_time = 0; // 上次量測的時間（毫秒）

void setup() {
  Serial.begin(9600);   // 與電腦（ROS2）通訊
  dht.begin();          // 啟動溫度感測器
}

void loop() {
  // 每 5 秒量一次
  if (millis() - pre_time >= 5000) {
    t = dht.readTemperature(); // 讀取溫度

    if (!isnan(t)) {           // 確認感測成功
      Serial.println(t);       // 傳送溫度值到 ROS2
    } else {
      Serial.println("Error"); // 感測失敗時輸出錯誤字串
    }

    pre_time = millis();       // 更新時間
  }
}
