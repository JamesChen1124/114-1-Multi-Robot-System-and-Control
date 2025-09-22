#include <Wire.h>
#include <BH1750FVI.h>
#include <LiquidCrystal_I2C.h>

// --- Light Sensor (BH1750) ---
BH1750FVI LightSensor;
const int ledPin = 13;  // LED pin

// --- LCD 20x4 (I2C address 0x27) ---
LiquidCrystal_I2C LCD(0x27, 20, 4);

// --- LCD Strings ---
String L0 =    "======= DEMO =======";
String L1 =    "==== Smart Home ====";
String L2 =    "====================";
String L3_1 =  "===== No Motion ====";
String L3_2 =  "====== Motion ======";

// --- Motion Sensor ---
#define MOTIONPIN 5

// --- Timer variable ---
unsigned long pre_time = 0;

void setup() {
  Serial.begin(9600);       // Start Serial Monitor
  pinMode(ledPin, OUTPUT);  // LED pin as output
  pinMode(MOTIONPIN, INPUT);// Motion sensor pin

  // --- Initialize BH1750 Light Sensor ---
  LightSensor.begin();
  LightSensor.SetAddress(Device_Address_L);
  LightSensor.SetMode(Continuous_H_resolution_Mode);

  // --- Initialize LCD ---
  LCD.begin();
  LCD.backlight();
  LCD.home();
  LCD.print(L0);
  LCD.setCursor(0, 1);
  LCD.print(L1);
  LCD.setCursor(0, 2);
  LCD.print(L2);
  LCD.setCursor(0, 3);
  LCD.print(L3_1);

  pre_time = millis();
}

void loop() {
  // --- Get Lux value from BH1750 ---
  int lux = LightSensor.GetLightIntensity();

  // Print Lux and LED state on Serial Monitor
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.print(" lux  |  ");

  if (lux < 150) {
    digitalWrite(ledPin, LOW);
    Serial.println("LED: ON");
  } else {
    digitalWrite(ledPin, HIGH);
    Serial.println("LED: OFF");
  }

  // --- Update LCD every 2 seconds ---
  if (millis() - pre_time >= 2000) {
    int motion = digitalRead(MOTIONPIN); // Read motion sensor
    if (motion) {
      LCD.setCursor(0, 3);
      LCD.print(L3_2);
    } else {
      LCD.setCursor(0, 3);
      LCD.print(L3_1);
    }

    // Update Lux value on LCD (row 2)
    LCD.setCursor(0, 2);
    LCD.print("Lux: ");
    LCD.print(lux);
    LCD.print("     "); // clear old values

 
    LCD.setCursor(0, 3);
    LCD.print("Motion: ");
    if (lux < 150){
      LCD.print(" ON          ");
    }else{
       LCD.print(" OFF          ");
      }

    pre_time = millis();
  }

  delay(1000); // Update rate for Serial Monitor
}
