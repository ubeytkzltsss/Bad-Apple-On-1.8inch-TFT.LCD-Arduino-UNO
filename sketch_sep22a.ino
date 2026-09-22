#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>

#define TFT_CS  10
#define TFT_DC  9
#define TFT_RST 8

#define WIDTH  128
#define HEIGHT 160

#define CHUNK 32
#define TOTAL_PIXELS (WIDTH * HEIGHT)
#define TOTAL_CHUNKS (TOTAL_PIXELS / CHUNK)

Adafruit_ST7735 tft(TFT_CS, TFT_DC, TFT_RST);

uint8_t buffer[CHUNK];

// RGB332 -> RGB565
uint16_t rgb332To565(uint8_t c) {

  uint8_t r = (c >> 5) & 0x07;
  uint8_t g = (c >> 2) & 0x07;
  uint8_t b = c & 0x03;

  r = (r * 255) / 7;
  g = (g * 255) / 7;
  b = (b * 255) / 3;

  return ((r & 0xF8) << 8) |
         ((g & 0xFC) << 3) |
         (b >> 3);
}

void setup() {

  Serial.begin(2000000);

  tft.initR(INITR_BLACKTAB);
  tft.setRotation(0);
  tft.fillScreen(ST77XX_BLACK);

  delay(1000);
}

void loop() {

  if (Serial.available() >= 2) {

    uint8_t a = Serial.read();
    uint8_t b = Serial.read();

    if (a != 0xAA || b != 0x55) {
      return;
    }

    Serial.write(0xCC);

    tft.startWrite();
    tft.setAddrWindow(0, 0, WIDTH, HEIGHT);

    for (int packet = 0; packet < TOTAL_CHUNKS; packet++) {

      while (Serial.available() < CHUNK) {
      }

      for (int i = 0; i < CHUNK; i++) {
        buffer[i] = Serial.read();
      }

      for (int i = 0; i < CHUNK; i++) {

        uint16_t color = rgb332To565(buffer[i]);

        tft.pushColor(color);
      }

      Serial.write(0xC1);
    }

    tft.endWrite();

    Serial.write(0xDD);
  }
}