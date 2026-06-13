from machine import ADC, Pin, UART, deepsleep
import time

# =========================
# --- USER SETTINGS ---
# =========================

DRY_VALUE = 2700  # Raw ADC value when soil is completely dry (adjust after calibration)
WET_VALUE = 1200  # Raw ADC value when soil is fully wet (adjust after calibration)

DRY_THRESHOLD = 40  # % moisture below which plant is considered "dry"
RECOVER_THRESHOLD = 55  # % moisture above which plant is considered "wet" again (hysteresis)

ALERT_TRACK = 1  # MP3 track number to play when dry (0001.mp3 = 1)

ALERT_DURATION = 5  # Seconds to wait to allow audio to finish playing

SLEEP_DRY = 600  # Seconds between checks when soil is dry
SLEEP_WET = 1800  # Seconds between checks when soil is healthy

VOLUME = 30  # DFPlayer volume (0–30)

# =========================
# --- SENSOR SETUP ---
# =========================

sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)


def read_average(samples=20):
    total = 0
    for _ in range(samples):
        total += sensor.read()
    return total // samples


def read_moisture():
    value = read_average()

    # Clamp values to expected range
    if value > DRY_VALUE:
        value = DRY_VALUE
    if value < WET_VALUE:
        value = WET_VALUE

    moisture = 100 - (((value - WET_VALUE) / (DRY_VALUE - WET_VALUE)) * 100)

    return value, moisture


# =========================
# --- DFPLAYER SETUP ---
# =========================

uart = UART(2, baudrate=9600, tx=17, rx=16)


def send_cmd(cmd, param=0):
    buf = bytearray([0x7E, 0xFF, 0x06, cmd, 0x00, (param >> 8) & 0xFF, param & 0xFF, 0xEF])
    uart.write(buf)


def set_volume(vol):
    send_cmd(0x06, vol)


def play(track):
    send_cmd(0x03, track)


# =========================
# --- MAIN LOGIC ---
# =========================

# Allow DFPlayer to boot properly
time.sleep(2)

set_volume(VOLUME)  # Volume level (0–30)

# Read moisture
raw_value, moisture = read_moisture()

print("Raw:", raw_value, " Moisture:", round(moisture, 1), "%")

# Decide if soil is dry
if moisture < DRY_THRESHOLD:
    print("Soil dry! Playing alert...")
    play(ALERT_TRACK)

    time.sleep(ALERT_DURATION)  # Allow audio to fully play before sleeping

    sleep_time = SLEEP_DRY  # Check more frequently when dry

elif moisture > RECOVER_THRESHOLD:
    print("Soil is sufficiently wet")

    sleep_time = SLEEP_WET  # Check less often when healthy

else:
    print("Moisture in transition zone")

    sleep_time = SLEEP_DRY  # Conservative: treat as dry-ish

# =========================
# --- SLEEP ---
# =========================

print("Sleeping for", sleep_time, "seconds...")


def sleep_s(seconds):
    deepsleep(seconds * 1000)


sleep_s(sleep_time)