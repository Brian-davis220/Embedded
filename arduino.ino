// Arduino Joystick Bluetooth
#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10, 11); // RX, TX (connect to HC-05 TX/RX)

const int joyX = A0;
const int joyY = A1;

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
}

void loop() {
  int xVal = analogRead(joyX); // 0-1023
  int yVal = analogRead(joyY);

  // Normalize to -1.0 to 1.0
  float x = (xVal - 512) / 512.0;
  float y = -(yVal - 512) / 512.0; // invert Y

  // Send data as "x,y\n"
  BTSerial.print(x);
  BTSerial.print(",");
  BTSerial.println(y);

  delay(50); // 20Hz
}
