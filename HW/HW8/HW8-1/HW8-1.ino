int ledPins[] = {2, 3, 4};  // 三顆 LED 分別接腳位 2、3、4
int total_leds = 3;

void setup() {
  Serial.begin(9600);  // 與 ROS 端通信
  for (int i = 0; i < total_leds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], HIGH);
  }
  Serial.println("Arduino ready");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();   // 讀取一個字元 ('1', '2', '3')
    int index = c - '1';      // 將字元轉成 LED index (0, 1, 2)
    if (index >= 0 && index < total_leds) {
      digitalWrite(ledPins[index], LOW);   // 亮起該腳位
      Serial.print("LED ");
      Serial.print(index + 1);
      Serial.println(" ON");
    }
  }
}
