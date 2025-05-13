# 🎛️ Stepper Motor Filament Winder (ESP8266 + A4988)

A MicroPython-based controller for winding 3D printer filament between spools using a stepper motor. This script runs on an ESP8266 (like a D1 Mini) with an A4988 driver.

It requires hardware input for:
- A **momentary button** for start/stop, speed and direction control. [Tact Button Switch 2 Pin DIP](https://amzn.eu/d/8XbbaUR)
- A **filament runout sensor** to stop when filament ends. [Micro Limit Switch](https://amzn.eu/d/gJHNqDW)

## ✨ Features

- 🧠 **Persistent settings** (direction and speed saved across reboots)
- ⏱️ **Smooth time-based motor ramping** (acceleration/deceleration)
- 🕵️‍♂️ **Filament runout detection** with debounce filtering
- 🚀 **Speed selection** via button during setup (slow/normal/fast)
- ↔️ **Direction toggle** via long button press (when filament is unloaded)
- 💡 **Dual LED indicators** for direction and filament presence
  - ⬅️ Left LED = Forward direction
  - ➡️ Right LED = Reverse direction
  - 🚨 Blinking = Motor active
  - 🔆 On (steady) = Filament loaded

---

## 📦 Hardware Setup

| Component            | Description                        |
|---------------------|------------------------------------|
| ESP8266 (D1 Mini)    | Microcontroller running MicroPython |
| A4988 Driver        | Controls stepper motor             |
| Stepper Motor       | NEMA17 or similar                  |
| Momentary Button    | Connected to RX (GPIO3)          |
| Runout Sensor       | Normally-open filament sensor to D7 (GPI13) |
| LEDs (PWM capable)  | Connected to D5 (GPIO14 - Right), D6 (GPIO12 - Left) |

🪛 **Wiring Notes:**
- Direction pin: D1 (GPIO5) -> A4988 DIR pin
- Step pin: D2 (GPIO4) -> A4988 STEP pin
- Enable pin: D3 (GPIO0) —> A4988 EN pin (LOW to enable)

---

## 🔧 How to Use

### 🎬 Startup LED Sequence
- During startup, LEDs flash.
- While flashing:
  - Press button quickly to cycle through speed levels.
    - 1 blink = Slow
    - 2 blinks = Normal
    - 3 blinks = Fast
  - Long-press the button (>2s) to toggle direction (only works if filament is NOT loaded).
    - Left LED = Forward
    - Right LED = Reverse

### ▶️ Starting the Motor
- Press the button while filament is loaded.
- Motor ramps up to cruising speed and runs until:
  - Button is pressed again, or
  - Filament runs out
- Direction LED blinks while motor is running

### 💾 Persistent Settings
- Settings are stored in config.json on the ESP8266.
- On each boot, last saved speed and direction are restored.

### 🔦 LED Behavior

| Condition                | LED L (Left) | LED R (Right) | Description         |
|-------------------------|--------------|----------------|---------------------|
| Filament loaded, forward | ON           | OFF           | Running forward     |
| Filament loaded, reverse | OFF          | ON            | Running reverse     |
| Filament missing         | OFF          | OFF           | Idle / waiting      |
| During running           | Blinks       | Blinks        | Active stepping     |

---

## 🧠 Improvements Over Basic Designs

- ✅ Uses **time-based ramping** instead of fixed delays
- ✅ **False runout events prevented** with sensor debounce logic
- ✅ **Speed and direction persist** even after power cycles
- ✅ One-button interface manages **start, stop, speed, and direction**
- ✅ **Direction and state feedback** through LED indicators

---

## 🚧 Next Steps / Ideas

- 📺 Add an OLED display for real-time speed and direction
- 📶 Switch to **ESP32** for Wi-Fi control and multitasking
- 🔁 Implement auto-winding with stall detection
- ⏲️ Timer to auto-stop after specific duration
- 🧠 Add EEPROM backup for fault tolerance
- 💪 Filament tension sensor integration
- 📊 Log winding activity or usage count to flash

---

## 📁 Files Included

- `main.py` - The full MicroPython script
- `config.json` - Auto-created file storing persistent settings

---

## ❤️ Credits

This project was developed and refined through iterative enhancement using MicroPython and hardware prototyping.

Inspired by LTS Designs incredible "LTS Respooler Motorized Filament Winder"
- https://lts-design.com/
- https://makerworld.com/en/models/448008-lts-respooler-motorized-filament-winder#profileId-354782

---

> Got suggestions or improvements? Submit a pull request or open an issue! Let's make winding smarter — together.
