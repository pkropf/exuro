// hacked by Peter Kropf (pkropf@gmail.com)
// based on the code from http://principialabs.com/arduino-python-4-axis-servo-control/

// Created:  23 December 2009
// Original Author:   Brian D. Wendt (http://principialabs.com/)
// Version:  1.0
// License:  GPLv3 (http://www.fsf.org/licensing/)

#include <Servo.h> 

#define SERVO_COUNT   4
#define LED_COUNT     1
#define PIN_COUNT     4

#define CMD_BLINK           0  // blink an led
#define CMD_SERVO           1  // move a servo
#define CMD_REGISTER_SWITCH 2  // register a switch on a pin
#define CMD_READ_SWITCH     3  // read the status of a switch, open / closed
#define CMD_PIN             4  // set a pin to the specified voltage


Servo servo[SERVO_COUNT];
int servo_pin[SERVO_COUNT];

int led[LED_COUNT];          // state of the led's
int led_counter[LED_COUNT];  // number of times remaining to toggle the led's
int led_pin[LED_COUNT];      // map of index id to led pin
long led_millis = 0;         // time the last blink happened

int minPulse = 600;   // minimum servo position, us (microseconds)
int maxPulse = 2400;  // maximum servo position, us

int startbyte;       // start byte, begin reading input
int cmd;             // what command are we doing?
int parm1;           // command parameter 1
int parm2;           // command parameter 2
int i;               // iterator

int relay_pin = 4;
int relay_state = LOW;


void setup()
{
  Serial.begin(9600);                    // setup the serial port for communications with the host computer

  for (i=0; i < SERVO_COUNT; i++) {      // initialize the servo_pin map to a known set of values
    servo_pin[i] = -1;
  }

  for (i=0; i < LED_COUNT; i++) {        // initialize the led_pin map to a known set of values
    led_pin[i] = -1;
    led_counter[i] = 0;
  }

  pinMode(relay_pin, OUTPUT);
  attachInterrupt(0, toggle_relay2, CHANGE);
  // attachInterrupt(0, toggle_relay, CHANGE);
  // attachInterrupt(0, relay_on, RISING);
  // attachInterrupt(0, relay_off, FALLING);
} 


void set_led(int pin, int blinks)
{
  int i;

  for (i=0; i < LED_COUNT; i++) {      // look for a matching servo
    if (led_pin[i] == pin) {
      led_counter[i] = blinks;
      break;
    }
  }

  if (i == LED_COUNT) {                // no servo found so add one to the first available slot
    for (i=0; i < LED_COUNT; i++) {
      if (led_pin[i] == -1) {
        led_pin[i] = pin;
        led_counter[i] = blinks;
        pinMode(pin, OUTPUT);
        break;
      }
    }
  }
}


void blink_leds()
{
  int i;
  unsigned long now = millis();

  if(now - led_millis > 1000) {
    led_millis = now;

    for (i=0; i < LED_COUNT; i++) {
      if (led_counter[i] > 0) {
        if (led[i] == LOW) {
          led[i] = HIGH;
        } else {
          led[i] = LOW;
          led_counter[i] = led_counter[i] - 1;
        }

        digitalWrite(led_pin[i], led[i]);
      }
    }
  }
}


void move_servo(int pin, int angle)
{
  int i;

  for (i=0; i < SERVO_COUNT; i++) {      // look for a matching servo
    if (servo_pin[i] == pin) {
      servo[i].write(angle);
      break;
    }
  }

  if (i == SERVO_COUNT) {                // no servo found so add one to the first available slot
    for (i=0; i < SERVO_COUNT; i++) {
      if (servo_pin[i] == -1) {
        servo_pin[i] = pin;
        servo[i].attach(pin, minPulse, maxPulse);
        servo[i].write(angle);
        break;
      }
    }
  }
}


void toggle_relay()
{
  relay_state = !relay_state;
}


void toggle_relay2()
{
  int val = digitalRead(2);

  if (val == LOW) {
    relay_state = LOW;
  } else {
    relay_state = HIGH;
  }
}

void relay_on()
{
  relay_state = HIGH;
}


void relay_off()
{
  relay_state = LOW;
}


void loop() 
{
  if (Serial.available() > 3) { // Wait for serial input (min 4 bytes in buffer)
    startbyte = Serial.read();
    if (startbyte == 255) {     // header byte to every command packet set
      cmd = Serial.read();      // what are we going to do?
      if (cmd == 255) {         // make sure it isn't a header byte
        return;
      }

      parm1 = Serial.read();    // get the first parameter
      if (parm1 == 255) {       // make sure it isn't a header byte
        return;
      }

      parm2 = Serial.read();    // get the second parameter
      if (parm2 == 255) {       // make sure it isn't a header byte
        return;
      }

      switch (cmd) {
          case CMD_BLINK:
            set_led(parm1, parm2);
            break;
          case CMD_SERVO:
            move_servo(parm1, parm2);
            break;
          case CMD_PIN:
            pinMode(parm1, OUTPUT);
            if (parm2 == 0) {
                digitalWrite(parm1, LOW);
            } else {
                digitalWrite(parm1, HIGH);
            }
            break;
          case CMD_REGISTER_SWITCH:
          case CMD_READ_SWITCH:
            break;
      }
    }
  }
  blink_leds();
  digitalWrite(relay_pin, relay_state);
}

