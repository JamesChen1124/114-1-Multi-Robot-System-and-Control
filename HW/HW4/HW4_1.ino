#define LEDPIN   3
#define BLUEPIN  5
#define REDPIN   7
#define GREENPIN 9
int lastR = 0, lastG = 255, lastB = 255; // default RED

void setup() {
  Serial.begin(9600);

  pinMode(LEDPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);
  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);

  digitalWrite(LEDPIN, HIGH);
  analogWrite(BLUEPIN, 255);
  analogWrite(REDPIN, 255);
  analogWrite(GREENPIN, 255);

  Serial.println("Type: RED / GREEN / BLUE / OFF");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim(); cmd.toUpperCase();

    if (cmd == "RED") {
      lastR = 0;   lastG = 255; lastB = 255; // R on, others off
      digitalWrite(LEDPIN, LOW);
      applyRGB();
      Serial.println("OK: RED");
    } else if (cmd == "GREEN") {
      lastR = 255; lastG = 0;   lastB = 255;
      digitalWrite(LEDPIN, LOW);
      applyRGB();
      Serial.println("OK: GREEN");
    } else if (cmd == "BLUE") {
      lastR = 255; lastG = 255; lastB = 0;
      digitalWrite(LEDPIN, LOW);
      applyRGB();
      Serial.println("OK: BLUE");
    } else if (cmd == "OFF") {
      digitalWrite(LEDPIN, HIGH);
      // keep channels off for clarity
      analogWrite(REDPIN,   255);
      analogWrite(GREENPIN, 255);
      analogWrite(BLUEPIN,  255);
      Serial.println("OK: OFF");
    } else if (cmd.length() > 0) {
      Serial.println("Use RED / GREEN / BLUE / OFF");
    }
  }
}

void applyRGB() {
  // Show color only when master is ON (LEDPIN LOW)
  if (digitalRead(LEDPIN) == LOW) {
    analogWrite(REDPIN,   lastR);
    analogWrite(GREENPIN, lastG);
    analogWrite(BLUEPIN,  lastB);
  } else {
    analogWrite(REDPIN,   255);
    analogWrite(GREENPIN, 255);
    analogWrite(BLUEPIN,  255);
  }
}
