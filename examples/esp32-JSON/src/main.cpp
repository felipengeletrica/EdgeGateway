#include <Arduino.h>
#include <ArduinoJson.h>

/* CONSTANTS */
#define BUFFER_JSON 2048
#define UUID                            \
  String((uint32_t)ESP.getEfuseMac()) + \
      String((uint32_t)(ESP.getEfuseMac() >> 32))
#define DEVICE_ID String("DEVICE_SAMPLE")
/* VARIABLES */
uint64_t uptime = 0;


void handleInterrupt() {
  uptime++;  // Sinaliza que a interrupção ocorreu
}

void setup() {
  
  Serial.begin(115200);
  // Configure a interrupção para ocorrer a cada 1 segundo (1000 milissegundos)
  attachInterrupt(digitalPinToInterrupt(2), handleInterrupt, FALLING);
  Serial.println("START JSON SAMPLE");
}

void loop() {

  // Create JSON object
  DynamicJsonDocument doc(BUFFER_JSON);

  // Fill JSON object with data
  doc["device_id"] = DEVICE_ID;
  doc["serial"] = UUID;
  doc["protocol_id"] = "0.1.0";
  doc["hw_ver"] = "hardware_version";
  doc["fw_ver"] = "firmware_version";
  doc["up_time"] = uptime++;

  JsonObject temp = doc.createNestedObject("temp");
  temp["TEMP1"] = random(30, 121);
  temp["TEMP2"] = random(30, 121);
  temp["TEMP3"] = random(30, 121);

  // Add troy and egito arrays as needed...

  JsonObject input = doc.createNestedObject("input");
  JsonObject analog = input.createNestedObject("analog");
  analog["AN1"] = random(0, 4097);
  analog["AN2"] = random(0, 4097);
  analog["AN3"] = random(0, 4097);
  analog["AN4"] = random(0, 4097);
  analog["AN5"] = random(0, 4097);
  analog["AN6"] = random(0, 4097);
  analog["AN7"] = random(0, 4097);
  analog["AN8"] = random(0, 4097);

  JsonObject digital = input.createNestedObject("digital");
  digital["DIG1"] = random(0, 2) == 0;
  digital["DIG2"] = random(0, 2) == 0;
  digital["DIG3"] = random(0, 2) == 0;
  digital["DIG4"] = random(0, 2) == 0;
  digital["DIG5"] = random(0, 2) == 0;
  digital["DIG6"] = random(0, 2) == 0;
  digital["DIG7"] = random(0, 2) == 0;
  digital["DIG8"] = random(0, 2) == 0;

  doc["ignition"] = random(0, 2) == 0;

  JsonObject can_pckg = doc.createNestedObject("can_pckg");
  can_pckg["can_id"] = "0x1234";
  can_pckg["dlc"] = 8;
  JsonArray msg = can_pckg.createNestedArray("msg");
  msg.add(random(0, 256));
  msg.add(random(0, 256));
  msg.add(random(0, 256));
  msg.add(random(0, 256));
  msg.add(random(0, 256));
  msg.add(random(0, 256));
  msg.add(random(0, 256));
  msg.add(random(0, 256));
  msg.add(random(0, 256));

  // Convert JSON object to string
  String jsonString;
  serializeJson(doc, jsonString);

  // Send JSON data via Serial
  Serial.println(jsonString);

  // Delay for 1 second
  delay(1000);
  Serial.println("Invalid data this not is json");
  delay(20);

}
