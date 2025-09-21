// sketch_sep08a
const int buzzerPin = 3;
const int sensorPin = 5;

void setup() {
  Serial.begin(9600);
  pinMode(buzzerPin, OUTPUT);
  pinMode(sensorPin, INPUT);
}

void loop() {
  int state = digitalRead(sensorPin);
  if (state == HIGH) {
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(buzzerPin, LOW);
  }
}
