import os
import time
import serial
from PIL import Image

PORT = "COM4"
BAUD = 2000000

FRAME_DIR = "frames"

WIDTH = 128
HEIGHT = 160

FPS = 10

CHUNK = 32

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=3,
    write_timeout=3
)


time.sleep(2)

ser.reset_input_buffer()
ser.reset_output_buffer()

print("Connecting to Arduino...")
print("Arduino is ready!")

frames = [
    f for f in os.listdir(FRAME_DIR)
    if f.lower().endswith(".png")
]

def get_number(name):
    try:
        return int(name.split("(")[1].split(")")[0])
    except:
        return 999999

frames.sort(key=get_number)

print("Frames are being prepared....")
print(f"{len(frames)} Frame found.")
print("THE VIDEO IS STARTING!")

frame_time = 1.0 / FPS

while True:

    for filename in frames:

        start = time.perf_counter()

        path = os.path.join(FRAME_DIR, filename)

        img = Image.open(path).convert("RGB")

        if img.size != (WIDTH, HEIGHT):
            img = img.resize(
                (WIDTH, HEIGHT),
                Image.Resampling.NEAREST
            )

        pixels = img.load()

        # RGB332:
        # 3 bit RED
        # 3 bit GREEN
        # 2 bit BLUE
        data = bytearray(WIDTH * HEIGHT)

        pos = 0

        for y in range(HEIGHT):

            for x in range(WIDTH):

                r, g, b = pixels[x, y]

                rgb332 = (
                    ((r >> 5) << 5) |
                    ((g >> 5) << 2) |
                    (b >> 6)
                )

                data[pos] = rgb332

                pos += 1

        # Frame start
        ser.write(b"\xAA\x55")

        response = ser.read(1)

        if response != b"\xCC":

            print(
                "\nError!",
                "",
                response
            )

            ser.reset_input_buffer()
            continue

        paket_hatasi = False

        for i in range(0, len(data), CHUNK):

            chunk = data[i:i + CHUNK]

            ser.write(chunk)

            response = ser.read(1)

            if response != b"\xC1":

                print(
                    f"\nPacket Error! "
                    f"Frame: {filename} "
                    f"Packet: {i // CHUNK}"
                )

                paket_hatasi = True
                break

        if paket_hatasi:
            ser.reset_input_buffer()
            continue

        response = ser.read(1)

        if response != b"\xDD":

            print(
                "\nFrame Error! "
                ""
            )

            ser.reset_input_buffer()
            continue

        elapsed = time.perf_counter() - start

        actual_fps = 1.0 / elapsed

        print(
            f"\r{filename} | "
            f"{actual_fps:.1f} FPS",
            end="",
            flush=True
        )

        wait = frame_time - elapsed

        if wait > 0:
            time.sleep(wait)

    print("\nstarting again....")