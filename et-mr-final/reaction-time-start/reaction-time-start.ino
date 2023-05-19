// Arduino file for the starting system and sending the start signal to python

int button = 3;
int sound = 6;
int led = 2;
int incomingByte;


void setup() {
  Serial.begin(115200);
  pinMode(led, OUTPUT);
  pinMode(sound, OUTPUT);
  pinMode(button, INPUT);
}

void loop() {
  // get the button state to determine if it is pressed
  int buttonState = digitalRead(button);

  // if button is pressed, send START to python
  // set off buzzer and light
  if(buttonState == 1) {
      Serial.println("START");
      digitalWrite(led, HIGH);
      tone(sound, 300);
      delay(400);
      noTone(sound);
      digitalWrite(led, LOW);
  }
    
}

