#define DCM1 11
#include "DHT.h"
#define TEMPIN 9
DHT dht(TEMPIN, DHT11);

void setup() {
  Serial.begin(9600);
  pinMode(DCM1, OUTPUT);
  analogWrite(DCM1, 0);
  dht.begin();
}

void loop() {
  float tem = dht.readTemperature();
  Serial.println(String("Temperature: ") + String(tem) + "°C");
  if (tem >= 25) {
    analogWrite(DCM1, 255);
  } else {
    analogWrite(DCM1, 0);
  }
  delay(1000);
}
