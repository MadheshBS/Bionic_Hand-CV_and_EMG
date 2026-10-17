#include <Servo.h>

// 5 servo objects — one per finger
Servo servos[5];

// PWM pins (use pins that support PWM on Uno)
const int PINS[5] = {10 , 3, 5 , 6, 9};
// 10 - Index, 3 - Middle, 5 - Ring, 6 - Pinky, 9 - Thumb
// Angles
const int ANGLE_OPEN   = 0;
const int ANGLE_FOLDED = 180;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) {
    servos[i].attach(PINS[i]);
    servos[i].write(ANGLE_OPEN);   // Start all fingers open
  }
}

void loop() {
  if (Serial.available() >= 5) {
    char buf[6];
    int len = Serial.readBytesUntil('\n', buf, 5);

    if (len == 5) {
      for (int i = 0; i < 5; i++) {
        if (buf[i] == '1') {
          servos[i].write(ANGLE_FOLDED);   // Fold finger
        } else if (buf[i] == '0') {
          servos[i].write(ANGLE_OPEN);     // Extend finger
        }
      }
    }
  }
}