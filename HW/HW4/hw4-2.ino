// 定義 LED 腳位
const int ledPins[8] = {2, 3, 4, 5, 6, 7, 8, 9}; // LED 1~8 分別接在腳位 2~9
bool ledStatus[8] = {false, false, false, false, false, false, false, false};

String inputString = "";  // 接收指令的字串
bool stringComplete = false;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 8; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], HIGH); // 預設關閉
  }
}

void loop() {
  if (stringComplete) {
    inputString.trim(); // 去掉空格

    // 分析指令，例如 "1 ON"
    int spaceIndex = inputString.indexOf(' ');
    if (spaceIndex > 0) {
      int ledNum = inputString.substring(0, spaceIndex).toInt();
      String action = inputString.substring(spaceIndex + 1);

      if (ledNum >= 1 && ledNum <= 8) {
        if (action == "ON") {
          digitalWrite(ledPins[ledNum - 1], LOW);
          ledStatus[ledNum - 1] = true;
        } else if (action == "OFF") {
          digitalWrite(ledPins[ledNum - 1], HIGH);
          ledStatus[ledNum - 1] = false;
        }
      }
    }

    // 回傳 LED 狀態
    String statusStr = "";
    for (int i = 0; i < 8; i++) {
      statusStr += String(i + 1) + ":" + (ledStatus[i] ? "ON" : "OFF") + " ";
    }
    Serial.println(statusStr);

    // 清空接收字串
    inputString = "";
    stringComplete = false;
  }
}

// 讀取 Serial
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}
