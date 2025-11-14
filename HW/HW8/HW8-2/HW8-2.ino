int motorPin = 9;
int pwmValue = 0;

void setup() {
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);
  analogWrite(motorPin, 0);
  Serial.println("Ready for PWM");
}

void loop() {
  if (Serial.available() > 0) {
    pwmValue = Serial.parseInt();
    pwmValue = constrain(pwmValue, 0, 255);
    analogWrite(motorPin, pwmValue);
    Serial.print("PWM set to: ");
    Serial.println(pwmValue);
    while (Serial.available() > 0)Serial.read();
  }
}


