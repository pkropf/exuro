// based on the code from http://principialabs.com/arduino-python-4-axis-servo-control/

// Copyright (c) 2011 Peter Kropf. All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

#include <Servo.h> 

#define SERVO_COUNT 4

Servo servo[SERVO_COUNT];
int servo_pin[SERVO_COUNT];

// Common servo setup values
int minPulse = 600;   // minimum servo position, us (microseconds)
int maxPulse = 2400;  // maximum servo position, us

// User input for servo and position
int userInput[3];    // raw input from serial buffer, 3 bytes
int startbyte;       // start byte, begin reading input
int pin;             // which pin to pulse?
int pos;             // servo angle 0-180
int i;               // iterator


void setup() 
{
  // initialize the servo_pin map to a known set of values
  for (i=0; i < SERVO_COUNT; i++) {
    servo_pin[i] = -1;
  }

  Serial.begin(9600);
} 


void loop() 
{ 
  // Wait for serial input (min 3 bytes in buffer)
  if (Serial.available() > 2) {
    // Read the first byte
    startbyte = Serial.read();
    // If it's really the startbyte (255) ...
    if (startbyte == 255) {
      // First byte = pin to pulse?
      pin = Serial.read();

      // Second byte = which position?
      pos = Serial.read();

      // Packet error checking and recovery
      if (pin == 255 || pos == 255) {
        return;
      }

      // look for the matching servo
      for (i=0; i < SERVO_COUNT; i++) {
        if (servo_pin[i] == pin) {
          servo[i].write(pos);
          break;
        }
      }

      // no servo found so add one to the first available slot
      if (i == SERVO_COUNT) {
        for (i=0; i < SERVO_COUNT; i++) {
          if (servo_pin[i] == -1) {
            servo_pin[i] = pin;
            servo[i].attach(pin, minPulse, maxPulse);
            servo[i].write(pos);    // move servo1 to 'pos'
            break;
          }
        }
      }
    }
  }
}
