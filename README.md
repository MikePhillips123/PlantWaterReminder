# <p align="center"><ins><strong>Plant Water Reminder</strong></ins></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3d9df03e-2312-4e18-876b-217f649bf5a3" width="600" alt="Completed Plant Water Reminder"/>
</p>

This project was created as a gift for my partner to help take the guesswork out of watering houseplants. Despite having many wonderful qualities, remembering to water plants isn't always one of them-and after joking that she has more of a brown thumb than a green one, I decided to build something that would remind her when her plants were actually thirsty.

The device is built around an ESP32 microcontroller and uses a capacitive soil moisture sensor to measure the water content of the soil. Rather than relying on LEDs or a mobile app, a DFPlayer Mini is used to play a pre-recorded voice message whenever the moisture level falls below a configurable threshold.

To maximise battery life, the ESP32 spends almost all of its time in deep sleep, only waking periodically to take a measurement before returning to sleep. The entire assembly is housed within a custom-designed 3D printed enclosure designed in Autodesk Fusion.

## <ins>Features</ins>

- ESP32 based control system
- Capacitive soil moisture sensing
- DFPlayer Mini audio notifications
- 18650 Li-Ion battery with onboard charging module
- Custom designed and fully 3D printable enclosure
- Low-power operation using ESP32 deep sleep
- Fully configurable moisture thresholds and wake intervals

## <ins>Hardware & Assembly</ins>

<p align="center">
<img src="https://github.com/user-attachments/assets/170aabeb-a0ff-4ed0-b73f-725775b5fe40" width="46%" alt="Exploded assembly"/>
<img src="https://github.com/user-attachments/assets/bf6bc593-7849-47dd-baca-33c694d7f6c1" width="46%" alt="Internal assembly"/>
</p>

The enclosure was designed from scratch in Autodesk Fusion with simplicity and ease of assembly in mind. It houses all of the electronics securely whilst remaining compact enough to sit discreetly alongside a plant pot.

The design accommodates:

- ESP32 development board
- DFPlayer Mini MP3 module
- Miniature loudspeaker
- TP4056 USB charging module
- Single 18650 Li-Ion rechargeable battery
- Capacitive soil moisture sensor

All components are secured using standard fasteners, allowing the enclosure to be easily opened for maintenance, battery replacement or future hardware upgrades.

## <ins>Software</ins>

The software is intentionally kept straightforward, making it easy to understand and customise for different plants or moisture sensors.

On each wake cycle the ESP32:

1. Powers up from deep sleep.
2. Takes multiple ADC readings from the capacitive moisture sensor.
3. Averages the readings to reduce electrical noise.
4. Converts the raw ADC value into an approximate moisture percentage using configurable wet and dry calibration values.
5. Compares the measured moisture level against user-defined thresholds.
6. Plays a configurable audio notification through the DFPlayer Mini if watering is required.
7. Returns to deep sleep for a configurable period before repeating the process.

Almost every aspect of the software can be customised through the constants defined at the top of `main.py`, including:

- Wet and dry calibration values
- Moisture thresholds
- Recovery threshold (preventing repeated alerts)
- Audio track number
- Playback duration
- Speaker volume
- Sleep intervals for wet and dry soil

This allows the device to be easily adapted to different plant species, soil types and moisture sensors without modifying the main program logic.

## <ins>Future Improvements</ins>

The current implementation successfully achieves the original design goals while keeping both the hardware and software intentionally simple.

However, several improvements could be made in future revisions, including:

- Battery voltage monitoring to provide a low-battery warning before charging is required.
- Automatic calibration routines for different moisture sensors.
- USB configuration utility for adjusting thresholds without modifying the source code.
- OLED status display.
- Bluetooth or Wi-Fi connectivity for remote monitoring.
- Logging moisture trends over time.
- Multiple selectable voice packs or notification sounds.
- Support for monitoring multiple plants from a single controller.

Although these features would add additional functionality, the current design already provides an efficient, low-power solution that can operate for extended periods from a single battery charge while requiring virtually no user interaction.
