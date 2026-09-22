# Bad Apple on Arduino TFT

Playing Bad Apple!! on a 128×160 ST7735 TFT using Arduino and Python.

## Installation

Clone the repository:

```bash
git clone https://github.com/ubeytkzltsss/Bad-Apple-On-1.8inch-TFT.LCD-Arduino-UNO.git
cd Bad-Apple-On-1.8inch-TFT.LCD-Arduino-UNO
```

Install the required Python libraries:

```bash
pip install pyserial pillow
```

## Wiring

| ST7735 TFT | Arduino UNO |
| ---------- | ----------- |
| VCC        | 5V          |
| GND        | GND         |
| SCL / SCK  | D13         |
| SDA / MOSI | D11         |
| CS         | D10         |
| DC / A0    | D9          |
| RST        | D8          |
| LED / BL   | 5V          |

## Usage

1. Upload the Arduino `.ino` file to the Arduino UNO.
2. Connect the ST7735 TFT using the pins above.
3. Make sure the `frames` folder contains the PNG frames.
4. Connect the Arduino to your PC.
5. Run:

```bash
python sender.py
```

The PNG frames will be sent from the PC to the Arduino and Bad Apple!! will play on the LCD display. 🎥


🎥 Video showcase below.


https://youtu.be/EluTrVv-Xh4


**Developed by Ubeyt**
