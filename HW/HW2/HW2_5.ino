const int redpin = 2;
const int greenpin = 4;
const int bluepin = 6;
const int ledpin = 8;
const int butpin = 10;
int state =0;

void setup() {
  pinMode(redpin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  pinMode(bluepin, OUTPUT);
  pinMode(ledpin, OUTPUT);
  pinMode(butpin, INPUT);
}

void loop() {
  state = digitalRead(butpin);

  if (state == LOW){
    digitalWrite(redpin, LOW);
    delay(1000);
    digitalWrite(redpin, HIGH);

    digitalWrite(greenpin, LOW);
    delay(2000);
    digitalWrite(greenpin, HIGH);

    digitalWrite(bluepin, LOW);
    delay(3000);
    digitalWrite(bluepin, HIGH);
  }

}
