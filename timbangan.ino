#include "HX711.h"

// Hardware Pin Definitions for ESP32
const int LOADCELL_DOUT_PIN = 26; // Board pin 'd26'
const int LOADCELL_SCK_PIN  = 27; // Board pin 'd27'
const int LED_PIN           = 2;  // Onboard blue LED ('d2')

// Calibration factor (replace with your calibrated value)
#define CALIBRATION_FACTOR -420.0 

HX711 scale;

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);

  Serial.println("\n=========================================");
  Serial.println("Initializing HX711 Scale System on ESP32");
  Serial.println("=========================================");

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(CALIBRATION_FACTOR);
  
  // Set initial zero point
  Serial.println("Taring scale... Ensure sensor is unloaded.");
  scale.tare();
  Serial.println("Tare Complete!\n");
}

void loop() {
  static unsigned long lastSensorRead = 0;
  static unsigned long lastBlink      = 0;
  static bool ledState                = false;

  unsigned long currentMillis = millis();

  // 1. Onboard LED blink ticker (500ms toggle)
  if (currentMillis - lastBlink >= 500) {
    lastBlink = currentMillis;
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
  }

  // 2. Read sensor every 500ms
  if (currentMillis - lastSensorRead >= 500) {
    lastSensorRead = currentMillis;

    if (scale.is_ready()) {
      float weight_g = scale.get_units(3); // Average of 3 readings

      // Noise floor filter near zero
      if (abs(weight_g) < 0.5) {
        weight_g = 0.0;
      }

      // Force calculation (F = m * g)
      float force_N = (weight_g / 1000.0) * 9.80665;

      Serial.print("Mass: ");
      Serial.print(weight_g, 1);
      Serial.print(" g  |  Force: ");
      Serial.print(force_N, 3);
      Serial.println(" N");
    } else {
      Serial.println("HX711 not responding... Check DOUT/SCK connection.");
    }
  }
}