/* This example shows how to display a moving gradient pattern on
 * an APA102-based LED strip. */

/* By default, the APA102 library uses pinMode and digitalWrite
 * to write to the LEDs, which works on all Arduino-compatible
 * boards but might be slow.  If you have a board supported by
 * the FastGPIO library and want faster LED updates, then install
 * the FastGPIO library and uncomment the next two lines: */
 #include <FastGPIO.h>
 #define APA102_USE_FAST_GPIO

#include <APA102.h>
#include "graphics.h"

// Define which pins to use.
const uint8_t dataPin = 11;
const uint8_t clockPin = 12;
const uint8_t irPin = 10;

int ledState = LOW;             // ledState used to set the LED
unsigned long previousMillis = 0;        // will store last time LED was updated
long OnTime = 1;           // milliseconds of on-time
long OffTime = 4;          // milliseconds of off-time


// Create an object for writing to the LED strip.
APA102<dataPin, clockPin> ledStrip;

// Set the number of LEDs to control.
const uint16_t ledCount = 72;

// Create a buffer for holding the colors (3 bytes per color).
rgb_color colors[ledCount];

// Set the brightness to use (the maximum is 31).
const uint8_t brightness = 1;

int myValues[] = {123, 456, 789};

// this for loop works correctly with an array of any type or size
uint16_t loopLimit = 50;//sizeof(green) / sizeof(green[0]);
int loopIteration = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(irPin,INPUT);
  
  for(uint16_t i = 0; i < ledCount; i++)
  {
    colors[i] = rgb_color(0, 0, 0);
  }

  ledStrip.write(colors, ledCount, brightness);

  //Serial.print(loopLimit);
}

void loop()
{
  unsigned long currentMillis = millis();
  
  if(digitalRead(irPin)==HIGH)
  {
    loopIteration = 0;
  }
  
  if(loopIteration < loopLimit) {
    if((ledState == LOW) && (currentMillis - previousMillis >= OffTime)) {
      ledState = HIGH;  // turn it on
      previousMillis = currentMillis; 

      for(uint8_t i = 0; i < ledCount; i++) {
        uint8_t redVal = (uint8_t *)pgm_read_word(&(red[loopIteration][i]));
        uint8_t greenVal = (uint8_t *)pgm_read_word(&(green[loopIteration][i]));
        uint8_t blueVal = (uint8_t *)pgm_read_word(&(blue[loopIteration][i]));
        //Serial.println(val);
        /*
        if(redVal < 100) {
          redVal = 0;
        } else {
          redVal = 255;
        }
  
        if(blueVal < 100) {
          blueVal = 0;
        } else {
          blueVal = 255;
        }
  
        if(greenVal < 100) {
          greenVal = 0;
        } else {
          greenVal = 255;
        }
        */
        
        
        colors[i] = rgb_color(redVal, greenVal, blueVal);
      }
    
      ledStrip.write(colors, ledCount, brightness);
      loopIteration = loopIteration + 1;
    } else if ((ledState == HIGH) && (currentMillis - previousMillis >= OnTime)) {
      ledState = LOW;  // turn it on
      previousMillis = currentMillis; 


      

      for(uint8_t i = 0; i < ledCount; i++) {
        colors[i] = rgb_color(0, 0, 0);
      }
      ledStrip.write(colors, ledCount, brightness);
    }
  } else {
    // do nothing and wait for the loopIteration to reset.
    //loopIteration = 0;
    for(uint8_t i = 0; i < ledCount; i++) {
        colors[i] = rgb_color(255, 255, 255);
      }
      ledStrip.write(colors, ledCount, brightness);
  } 
    
    
}
