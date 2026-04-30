#include <Arduino.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_ADDRESS 0x3C // This is the default I2C address for 128x64 OLEDs
Adafruit_SSD1306 display(128, 64);

void setup() {
  Wire.begin();
  
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) { // Address 0x3C for 128x64
    Serial.println(F("Couldn'<beginofsentence>t find display"));
  }
  
  display.clearDisplay();
}

void loop() {
  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(WHITE); // Draw white text
  display.setCursor(0, 20);    // Start at top-left corner
  display.println("Hello world!");
  display.display();            // Show it on the screen
}