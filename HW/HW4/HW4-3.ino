#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

const int DCM1 = 2;
const int DCM2 = 3;

String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(9600);

  pinMode(DCM1, OUTPUT);
  pinMode(DCM2, OUTPUT);

  digitalWrite(DCM1, LOW);
  digitalWrite(DCM2, LOW);

  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("DC Motor Ready");
}

void loop() {
  if (stringComplete) {
    inputString.trim();
    int spaceIndex = inputString.indexOf(' ');

    if (spaceIndex > 0) {
      String dir = inputString.substring(0, spaceIndex);
      int pwmVal = inputString.substring(spaceIndex + 1).toInt();
      pwmVal = constrain(pwmVal, 0, 255);

      if (dir == "CW") {
        digitalWrite(DCM1, HIGH);
        digitalWrite(DCM2, LOW);

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Dir: CW");
        lcd.setCursor(0, 1);
        lcd.print("PWM: " + String(pwmVal));
        Serial.print("CW, PWM=");
        Serial.println(pwmVal);
      }
      else if (dir == "CCW") {
        digitalWrite(DCM1, LOW);
        digitalWrite(DCM2, HIGH);
      
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Dir: CCW");
        lcd.setCursor(0, 1);
        lcd.print("PWM: " + String(pwmVal));
        Serial.print("CCW, PWM=");
        Serial.println(pwmVal);
      }
      else {
        digitalWrite(DCM1, LOW);
        digitalWrite(DCM2, LOW);
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Invalid CMD");
        Serial.println("Invalid command! Use CW or CCW.");
      }
    }

    inputString = "";
    stringComplete = false;
  }
}

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
