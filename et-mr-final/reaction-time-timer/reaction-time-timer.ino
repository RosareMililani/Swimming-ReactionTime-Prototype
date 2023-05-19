// Arduino file for the timing and touch sensor

int led = 3;
int incomingByte;
int touch = 2;
int sound = 7;
int starttime;
int endtime;
int reactiontime;

void setup() {
  pinMode(led, OUTPUT);
  Serial.begin(115200);
  pinMode(touch, INPUT_PULLUP);
  pinMode(sound, OUTPUT);
  // attach an interrupt to the touch sensor, so that the endtimer() fires when the sensor is released
  attachInterrupt(digitalPinToInterrupt(touch), endtimer, FALLING);
}

void loop() {
  // read in the bytes from python
   incomingByte = Serial.read();

  // if S, start the timer
  // the lght is for testing purposes
  if(incomingByte == 'S') {
    starttime = millis();
    digitalWrite(led, HIGH);
    delay(400);
    digitalWrite(led, LOW);
  }

  //If F, this will fire as the false start alarm 
  if(incomingByte == 'F'){
    for(int i = 0; i < 3; i++) {
     // digitalWrite(led, HIGH);
      tone(sound, 300);
      delay(400);
      noTone(sound);   
      delay(200);
    }
  }
}


// Function to get the end time and calculate the end time
// Sends command TIME to python so it knows the reaction time is coming
// send reaction time to python 
void endtimer() {
  digitalWrite(led, LOW);
  endtime = millis();
  reactiontime = endtime - starttime;
  Serial.println("TIME");
  Serial.println(reactiontime);

}