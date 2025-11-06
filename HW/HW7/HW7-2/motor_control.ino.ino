#define DCM1 3
#define MOTIONPIN 5

unsigned long pre_time = 0;
unsigned long pre_time2 = 0;
bool motion_status = false;

void setup() {
  pinMode(DCM1, OUTPUT);
  pinMode(MOTIONOIN, INPUT);
  digitalWrite(DCM1, LOW);  
  Serial.begin(9600);
  pre_time = millis();
}

void loop() {
  if (millis() - pre_time >= 1000) {  
    int x = digitalRead(MOTIONPIN); 
    if (x && !motion_status)  {
      digitalWrite(DCM1, HIGH);
      motion_status = true;
      Serial.println('motor on')
      pre_time2 = millis();
    }
    if (!x && (millis() - pre_time2 >= 10000))  {
      digitalWrite(DCM1, LOW);
      motion_status = false;
      Serial.println('motor off')
    }
    pre_time = millis();
  }
}
