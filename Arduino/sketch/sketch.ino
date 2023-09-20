#include "Wire.h"
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

#define I2C_ADDRESS 0x04
#define MICROPHONE_PIN 0

// lorawan setup
// appEUI from TTN reversed
static const u1_t PROGMEM APPEUI[8]={ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8); }

// devEUI from TTN reversed
static const u1_t PROGMEM DEVEUI[8]={ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8); }

// appKey from TTN
static const u1_t PROGMEM APPKEY[16] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
void os_getDevKey (u1_t* buf) { memcpy_P(buf, APPKEY, 16); }
static osjob_t sendjob;

// 0 - ready, 1 - busy, 2 - error (could not connect)
int state = 1;

// Pin mapping
const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 6,
    .dio = {9, 8, 7},
};

void onEvent (ev_t ev) {
    switch(ev) {
        case EV_SCAN_TIMEOUT:
            state = 2;
            break;
        case EV_BEACON_FOUND:
            break;
        case EV_BEACON_MISSED:
            break;
        case EV_BEACON_TRACKED:
            break;
        case EV_JOINING:
            break;
        case EV_JOINED:
            // Disable link check validation (automatically enabled
            // during join, but not supported by TTN at this time).
            LMIC_setLinkCheckMode(0);
            break;
        case EV_RFU1:
            break;
        case EV_JOIN_FAILED:
            state = 2;
            break;
        case EV_REJOIN_FAILED:
            state = 2;
            break;
        case EV_TXCOMPLETE:
            state = 0;
            break;
        case EV_LOST_TSYNC:
            break;
        case EV_RESET:
            break;
        case EV_RXCOMPLETE:
            break;
        case EV_LINK_DEAD:
            break;
        case EV_LINK_ALIVE:
            break;
         default:
            break;
    }
}

void sendMessage(osjob_t* j, uint8_t* data, int dataLength){
    // Wait for current TX/RX job finish
    while (LMIC.opmode & OP_TXRXPEND) 
    {
      delay(100);
    }
    
    // Prepare upstream data transmission at the next possible time.
    LMIC_setTxData2(1, data, dataLength, 0);
    Serial.println(F("Packet queued"));
}

void setup() {
  // I2c
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveMessage);
  Wire.onRequest(sendState);
  
  // LMIC init
//  os_init();
  // Reset the MAC state. Session and pending data transfers will be discarded.
//  LMIC_reset();

  state = 0;
}


void loop() {
  os_runloop_once();
  // max9814 putputs data in range 0-530 with bias at aproximetely 265
}


// callback for received data
void receiveMessage(int byteCount){
  uint8_t message[byteCount];
  
  for (short i = 0; i < byteCount; i++) {
    message[i] = Wire.read();
  }

  state = 1;
//  sendMessage(&sendjob, message, byteCount);
}

// callback for sending data
void sendState(){
  Wire.write(state);
}
