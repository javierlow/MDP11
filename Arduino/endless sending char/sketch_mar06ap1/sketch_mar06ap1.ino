void setup(){
  Serial.begin(115200);
}

void loop(){
  //Serial.println("T Test");   
  delay(2000);


   while (Serial.available()) {
    // get the new byte:
    String robotRead = Serial.readString();
    char c = robotRead.charAt(0)+1;
    String s = String(s+c);
    Serial.println("P" +s );
}
}
