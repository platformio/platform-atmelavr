#include <Arduino.h>
// Spin around in goovy HSB color space
// HSB stands for Hue, Saturation, and Brightness
// https://en.wikipedia.org/wiki/HSL_and_HSV

void setup() {
  // No setup needed for this simple example!  
}

byte hue=0;

Timer nextStep;

void loop() {

  if (nextStep.isExpired()) {

    // Spin the hue while keeping color saturation and brightness at max  
    setColor( makeColorHSB( hue , 255 , 255 ) );
    
    // Becuase we are using an 8-bit byte for the `hue` variable, 
    // this will automatically roll over from 255 back down to 0  
    // (255 is 11111111 in binary, and 11111111 + 00000001 = 00000000)
    hue++;      

    nextStep.set(10);     // Step to (slightly) different color 100 times per second - whole cycle will take 255 steps *10ms = ~2.5 seconds. 

  }

}
