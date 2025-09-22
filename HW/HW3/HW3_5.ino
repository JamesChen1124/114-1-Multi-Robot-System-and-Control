
void setup() {
  Serial.begin(9600);
  Serial.println("Type something and press Enter.");
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    Serial.println(line);
  }
}
