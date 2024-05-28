#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <BLECharacteristic.h>
#include <BLEUUID.h>
#include <ArduinoJson.h>

/* CONSTANTS */
// Hardware Serial 2 pins
#define TIMER_INTERRUPT_US 1000000
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define RXD2 6
#define TXD2 7
#define SIZE_BUFFER 2048
#define BUFFER_JSON SIZE_BUFFER
#define UUID                            \
  String((uint32_t)ESP.getEfuseMac()) + \
      String((uint32_t)(ESP.getEfuseMac() >> 32))
#define DEVICE_ID String("belfast_test")
/* VARIABLES */
uint64_t uptime = 0;
// Handle do timer
esp_timer_handle_t timer_handle;
BLEServer *pServer;
BLECharacteristic *pCharacteristic;
bool deviceConnected = false;

class MyServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer *pServer) {
        deviceConnected = true;
    }

    void onDisconnect(BLEServer *pServer) {
        deviceConnected = false;
    }
};


/**
 * @brief Interrupt 
 * 
 * @param arg 
 */
void timer_callback(void* arg) {
    uptime++;
}

void setup() {
    Serial.begin(115200);

    BLEDevice::init("ESP32 BLE Belfast");
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());

    BLEService *pService = pServer->createService(SERVICE_UUID);
    pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_NOTIFY
    );

    pCharacteristic->addDescriptor(new BLE2902());

    pService->start();
    BLEAdvertising *pAdvertising = pServer->getAdvertising();
    pAdvertising->start();

    // Configuração do timer
    esp_timer_create_args_t timer_args;
    timer_args.callback = &timer_callback;
    timer_args.arg = NULL;
    timer_args.dispatch_method = ESP_TIMER_TASK;
    timer_args.name = "periodic_timer";

    // Criar e iniciar o timer
    esp_timer_create(&timer_args, &timer_handle);
    esp_timer_start_periodic(timer_handle, TIMER_INTERRUPT_US);

    // Configurar MTU
    BLEDevice::setMTU(SIZE_BUFFER);

    Serial.println("START BLE SAMPLE");
}

void loop() {
    if (deviceConnected) {
        // Create JSON object
        DynamicJsonDocument doc(BUFFER_JSON);

        // Fill JSON object with data
        doc["device_id"] = DEVICE_ID;
        doc["serial"] = UUID;
        doc["protocol_id"] = "0.1.0";
        doc["hw_ver"] = "hardware_version";
        doc["fw_ver"] = "firmware_version";
        doc["up_time"] = uptime;

        // Convert JSON object to string
        String jsonString;
        serializeJson(doc, jsonString);

        // Send JSON data via Serial
        Serial.println(jsonString);

        pCharacteristic->setValue(jsonString.c_str());
        pCharacteristic->notify();
        Serial.println(jsonString);
        delay(100);
    }
}
