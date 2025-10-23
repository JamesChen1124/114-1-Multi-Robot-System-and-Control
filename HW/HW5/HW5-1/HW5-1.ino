#include "DHT.h"

DHT dht(2, DHT11);          // DHT11接pin 2
float t = 0.0;             
unsigned long pre_time = 0; 

void setup() {
  Serial.begin(9600);   
  dht.begin();         
}

void loop() {
  if (millis() - pre_time >= 5000) {
    t = dht.readTemperature(); 

    if (!isnan(t)) {           
      Serial.println(t);       
    } else {
      Serial.println("Error");
    }

    pre_time = millis();      
  }
}
