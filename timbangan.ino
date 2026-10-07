#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include "HX711.h"

// Hardware Pin Definitions
const int LOADCELL_DOUT_PIN = 26; // Board pin 'd26'
const int LOADCELL_SCK_PIN  = 27; // Board pin 'd27'
const int LED_PIN           = 2;  // Onboard blue LED ('d2')

// Calibration factor (replace with your calibrated factor)
#define CALIBRATION_FACTOR -420.0 

// SoftAP Wi-Fi Credentials
const char* ssid     = "ESP32-Scale-AP";
const char* password = "password123";

// System Global Variables
float currentWeight_g = 0.0;
float currentForce_N  = 0.0;
unsigned long blinkInterval = 500; // Default: 500 ms (< 150g)

HX711 scale;
AsyncWebServer server(80);

// Single Page Application (HTML + Dynamic JS Fetch)
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML>
<html>
<head>
  <title>ESP32 Weight Scale</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f9; padding: 20px; }
    .card { background: white; max-width: 400px; margin: auto; padding: 20px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    h1 { color: #333; margin-bottom: 5px; }
    .reading { font-size: 2.5rem; font-weight: bold; color: #007bff; margin: 15px 0; }
    .unit { font-size: 1.2rem; color: #666; }
    .status { font-size: 0.9rem; color: #28a745; margin-top: 10px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Live Scale Reading</h1>
    <p class="reading"><span id="weight">0.0</span> <span class="unit">g</span></p>
    <p class="reading" style="color: #6c757d;"><span id="force">0.000</span> <span class="unit">N</span></p>
    <div class="status">&#9679; Connected to ESP32 Scale</div>
  </div>
  <script>
    setInterval(function() {
      fetch('/data').then(response => response.json()).then(data => {
        document.getElementById('weight').innerText = data.weight.toFixed(1);
        document.getElementById('force').innerText  = data.force.toFixed(3);
      });
    }, 300); // Poll readings every 300ms
  </script>
</body>
</html>
)rawliteral";

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  // 1. Initialize Scale
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(CALIBRATION_FACTOR);
  scale.tare();

  // 2. Configure SoftAP & Internal DHCP Server
  WiFi.softAP(ssid, password);
  // Disable sending Default Gateway (Option 3) to DHCP clients
  uint8_t dhcp_offer_option = ROUTER_OFFER_DISABLE;
  dhcps_change_option(
    OFFER_ROUTER, 
    &dhcp_offer_option, 
    sizeof(dhcp_offer_option)
  );
  Serial.println("DHCP server configured: Gateway option disabled.");
  IPAddress IP = WiFi.softAPIP();
  Serial.println("\n=========================================");
  Serial.print("Access Point Started! Network Name: ");
  Serial.println(ssid);
  Serial.print("Webserver URL: http://");
  Serial.println(IP);
  Serial.println("=========================================");

  // 3. Webserver Routes
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html);
  });

  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request){
    String json = "{\"weight\":" + String(currentWeight_g, 1) + ",\"force\":" + String(currentForce_N, 3) + "}";
    request->send(200, "application/json", json);
  });

  server.begin();
}

void loop() {
  unsigned long currentMillis = millis();
  static unsigned long lastSensorRead = 0;
  static unsigned long lastBlink      = 0;
  static bool ledState                = false;

  // 1. Read Sensor Every 200 ms
  if (currentMillis - lastSensorRead >= 200) {
    lastSensorRead = currentMillis;

    if (scale.is_ready()) {
      currentWeight_g = scale.get_units(2); // Average of 2 samples

      if (abs(currentWeight_g) < 0.5) {
        currentWeight_g = 0.0;
      }
      currentForce_N = (currentWeight_g / 1000.0) * 9.80665;

      // Update LED blink frequency threshold (150 g)
      if (currentWeight_g > 150.0) {
        blinkInterval = 3000; // Blink every 3 seconds
      } else {
        blinkInterval = 500;  // Blink every 500 ms
      }
    }
  }

  // 2. Non-Blocking Dynamic LED Blink Execution
  if (currentMillis - lastBlink >= blinkInterval) {
    lastBlink = currentMillis;
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
  }
}