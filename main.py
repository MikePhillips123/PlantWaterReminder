from machine import ADC, Pin, UART, deepsleep
import time

# =========================
# --- USER SETTINGS ---
# =========================

DRY_VALUE = 2700
WET_VALUE = 1200

DRY_THRESHOLD = 40
RECOVER_THRESHOLD = 55

ALERT_TRACK = 1
ALERT_DURATION = 5

SLEEP_DRY = 600
SLEEP_WET = 3600

VOLUME = 30

# =========================
# Startup delay
# =========================

print("Starting in 5 seconds...")
print("Press Ctrl+C in Thonny to stop execution.")

time.sleep(5)

# =========================
# Sensor setup
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

    value = min(max(value, WET_VALUE), DRY_VALUE)

    moisture = 100 - (
        ((value - WET_VALUE) /
         (DRY_VALUE - WET_VALUE)) * 100
    )

    return value, moisture


# =========================
# DFPlayer setup
# =========================

uart = UART(2, baudrate=9600, tx=17, rx=16)


def send_cmd(cmd, param=0):
    buf = bytearray([
        0x7E,
        0xFF,
        0x06,
        cmd,
        0x00,
        (param >> 8) & 0xFF,
        param & 0xFF,
        0xEF
    ])
    uart.write(buf)


def set_volume(vol):
    send_cmd(0x06, vol)


def play(track):
    send_cmd(0x03, track)


# Allow DFPlayer to initialise
time.sleep(2)
set_volume(VOLUME)

# =========================
# Read moisture
# =========================

raw_value, moisture = read_moisture()

print("--------------------------------")
print("Raw:", raw_value)
print("Moisture:", round(moisture, 1), "%")

# =========================
# Decision
# =========================

if moisture < DRY_THRESHOLD:

    print("Soil dry! Playing alert...")

    play(ALERT_TRACK)

    time.sleep(ALERT_DURATION)

    sleep_time = SLEEP_DRY

elif moisture > RECOVER_THRESHOLD:

    print("Soil is sufficiently wet")

    sleep_time = SLEEP_WET

else:

    print("Moisture in transition zone")

    sleep_time = SLEEP_DRY

print("Entering deep sleep for", sleep_time, "seconds...")

# Give the UART time to finish transmitting
time.sleep(0.5)

deepsleep(sleep_time * 1000)