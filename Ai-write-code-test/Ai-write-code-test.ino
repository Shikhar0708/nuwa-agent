#include <Arduino.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


// Define the OLED display size and I2C address
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDRESS 0x3C

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  // Initialize I2C and start the wire library
  Wire.begin();
  
  // Initialize the OLED display
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("Could not initialize OLED"));
    while (1);
  }
}

void loop() {
  // Clear the display
  display.clearDisplay();
  
  // Write text to the display
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0, 15);
  display.println("Nuwa is great at coding");
  
  // Display the updated text
  display.display();
}