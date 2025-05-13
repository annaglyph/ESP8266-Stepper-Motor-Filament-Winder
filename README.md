# 🎛️ ESP8266 Stepper Motor Filament Winder

This MicroPython-based project runs on an ESP8266 (e.g., Wemos D1 Mini) and controls a stepper motor via an A4988 driver to wind 3D printer filament from one spool to another.

It includes hardware input for:
- A **momentary button** for start/stop, speed and direction control. [Tact Button Switch 2 Pin DIP] (https://amzn.eu/d/8XbbaUR)
- A **filament runout sensor** to stop when filament ends. [Micro Limit Switch](https://amzn.eu/d/gJHNqDW))

## ✨ Features

- 🧠 **Persistent settings** (direction and speed saved across reboots)
- ⏱️ **Smooth time-based motor ramping** (acceleration/deceleration)
- 🧵 **Filament runout detection** with debounce filtering
- 🎛️ **Speed selection** via button during setup (slow/normal/fast)
- 🔁 **Direction toggle** via long button press (when filament is unloaded)
- 💡 **Dual LED indicators** for direction and filament presence

---

## 📦 Hardware Setup

| Component            | Description                        |
|---------------------|------------------------------------|
| ESP8266 (D1 Mini)    | Microcontroller running MicroPython |
| A4988 Driver        | Controls stepper motor             |
| Stepper Motor       | NEMA17 or similar                  |
| Momentary Button    | Connected to RX (GPIO3)          |
| Runout Sensor       | Normally-closed filament sensor to D7 (GPI13) |
| LEDs (PWM capable)  | Connected to D5 (GPIO14 - Right), D6 (GPIO12 - Left) |

🪛 **Wiring Notes:**
- Direction pin: D1 (GPIO5)
- Step pin: D2 (GPIO4)
- Enable pin: D3 (GPIO0) — LOW to enable

---

## 🔧 How to Use

### ▶️ Starting the Motor
- Press the button while filament is loaded
- Motor ramps up and runs until:
  - Button is pressed again, or
  - Filament runs out

### ⏩ Changing Speed
- Hold the button while powering on
- LEDs will cycle to indicate speed level:
  - 1 blink = Slow
  - 2 blinks = Normal
  - 3 blinks = Fast
- Release the button on the desired mode
- Setting is saved in memory

### 🔁 Reversing Direction
- Long-press the button (1.5s) **only when filament is NOT loaded**
- Direction will toggle
- Left LED = Forward
- Right LED = Reverse
- Saved in memory

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

Here are some ideas to expand the project:
- 📺 Add an OLED display for real-time speed and direction
- 📶 Switch to **ESP32** for Wi-Fi control and multitasking
- 🔁 Implement auto-winding with stall detection
- 🧠 Add EEPROM backup for fault tolerance
- 📊 Log winding activity or usage count to flash

---

## 📁 Files Included

- `main.py` - The full MicroPython script
- `config.json` - Auto-created file storing persistent settings

---

## ❤️ Credits

This project was developed and refined through iterative enhancement using MicroPython and hardware prototyping.
Inspired by LTS Designs incredible "LTS Respooler Motorized Filament Winder".
https://lts-design.com/
https://makerworld.com/en/models/448008-lts-respooler-motorized-filament-winder#profileId-354782

---

> Got suggestions or improvements? Submit a pull request or open an issue! Let's make winding smarter — together.
