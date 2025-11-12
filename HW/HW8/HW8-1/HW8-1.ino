int ledPins[] = {2, 3, 4};  
int total_leds = 3;

void setup() {
  Serial.begin(9600); 
  for (int i = 0; i < total_leds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], HIGH);
  }
  Serial.println("Arduino ready");
}
void loop() {
  if (Serial.available()) {
    char c = Serial.read();   
    int index = c - '1';    
    if (index >= 0 && index < total_leds) {
      digitalWrite(ledPins[index], LOW);   
      Serial.print("LED ");
      Serial.print(index + 1);
      Serial.println(" ON");
    }
  }
}
