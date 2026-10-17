#include <Servo.h>

// Servo objects
Servo s1, s2, s3, s4, s5;

// EMG pin
const int emgPin = A0;

// Smoothing variables
float smooth = 0;

// Thresholds (you MUST calibrate this)
int HIGH_THRESHOLD = 1020;
int LOW_THRESHOLD  = 1000;

// State control
bool handClosed = false;

// Hold timing (prevents flicker)
unsigned long lastTriggerTime = 0;
int holdTime = 500; // milliseconds

void setup() {
  Serial.begin(9600);

  // Attach servos (change pins if needed)
  s1.attach(3);
  s2.attach(5);
  s3.attach(6);
  s4.attach(9);
  s5.attach(10);

  openHand(); // start open
}

void loop() {
  int raw = analogRead(emgPin);

  // Exponential smoothing
  smooth = 0.9 * smooth + 0.1 * raw;

  Serial.println(smooth);

  // Hysteresis control
  if (smooth > HIGH_THRESHOLD) {
    handClosed = true;
    lastTriggerTime = millis();
  }
  else if (smooth < LOW_THRESHOLD) {
    // only open after hold time
    if (millis() - lastTriggerTime > holdTime) {
      handClosed = false;
    }
  }

  // Apply movement
  if (handClosed) {
    closeHand();
  } else {
    openHand();
  }
}

// 🔓 Open hand
void openHand() {
  s1.write(0);
  s2.write(0);
  s3.write(0);
  s4.write(0);
  s5.write(0);
}

// ✊ Close hand
void closeHand() {
  s1.write(180);
  s2.write(180);
  s3.write(180);
  s4.write(180);
  s5.write(180);
}