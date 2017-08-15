int sensorPin = A0;
//int distance = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(sensorPin,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  //int data = analogRead(sensorPin);
  //int volt = map(data,0,1023,0,5000);
  //distance = (21.61/(volt-0.1696))*1000;
  float distance = 12343.85 * pow(analogRead(sensorPin),-1.15);
  Serial.println(distance);
  //if(Serial.available()){
  //  Serial.write(distance);
  delay(500);
  //}
}
