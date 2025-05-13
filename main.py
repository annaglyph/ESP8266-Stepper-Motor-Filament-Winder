from machine import Pin, PWM
import time
import ujson
import os

# -------------------------------
# Configuration & Defaults
# -------------------------------
CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "speed_level": 1,     # 0=slow, 1=normal, 2=fast
    "direction": 1        # 1=forward, 0=reverse
}

SPEED_LEVELS = {
    0: 400,   # Slow (safe for most motors)
    1: 300,   # Normal
    2: 200    # Fast
}

ACCEL_DURATION = 2000      # ms to reach cruise speed
STEP_INTERVAL_MIN = 100    # Min safe delay between steps (μs)
SENSOR_DEBOUNCE_MS = 150   # ms duration sensor must stay untriggered
LONG_PRESS_TIME = 2000     # ms for long press detection
LED_BRIGHTNESS = 50        # PWM duty (0-1023)

# -------------------------------
# Hardware Setup (D1 Mini pins)
# -------------------------------
button = Pin(13, Pin.IN, Pin.PULL_UP)
sensor = Pin(3, Pin.IN, Pin.PULL_UP)
led_l = PWM(Pin(12), freq=1000)
led_r = PWM(Pin(14), freq=1000)
en = Pin(0, Pin.OUT)
stp = Pin(4, Pin.OUT)
dir = Pin(5, Pin.OUT)

# -------------------------------
# Configuration Persistence
# -------------------------------
def load_config():
    if CONFIG_FILE in os.listdir():
        with open(CONFIG_FILE) as f:
            return ujson.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        ujson.dump(cfg, f)

config = load_config()

# -------------------------------
# LED Control
# -------------------------------
def set_led(pwm, brightness):
    pwm.duty(brightness)

def clear_leds():
    led_l.duty(0)
    led_r.duty(0)

def show_direction():
    """Illuminate LED based on motor direction."""
    if config["direction"]:
        set_led(led_l, LED_BRIGHTNESS)
        led_r.duty(0)
    else:
        set_led(led_r, LED_BRIGHTNESS)
        led_l.duty(0)

def blink_led(pwm, delay_ms):
    """Blink the given LED with specified interval."""
    current = time.ticks_ms()
    if not hasattr(blink_led, "last"):
        blink_led.last = 0
    if time.ticks_diff(current, blink_led.last) >= delay_ms:
        blink_led.last = current
        pwm.duty(0 if pwm.duty() else LED_BRIGHTNESS)

# -------------------------------
# Motor & Sensor Helpers
# -------------------------------
def step_once(delay_us):
    """Send a single step pulse."""
    stp.on()
    time.sleep_us(delay_us)
    stp.off()
    time.sleep_us(delay_us)

def filament_loaded():
    return sensor.value() == 0  # Assuming normally-open switch

def wait_sensor_clear(delay_us):
    """Debounce the runout sensor."""
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < SENSOR_DEBOUNCE_MS:
        step_once(delay_us)
        if filament_loaded():
            return False
    return True

# -------------------------------
# Ramping Logic (time-based)
# -------------------------------
def ramp_motor(target_delay):
    """Accelerate to target speed over fixed time."""
    start_time = time.ticks_ms()
    current_delay = target_delay + 300

    while current_delay > target_delay:
        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, start_time)
        if elapsed >= ACCEL_DURATION:
            break
        # Linear interpolation
        progress = elapsed / ACCEL_DURATION
        current_delay = int((1 - progress) * (target_delay + 300) + progress * target_delay)
        current_delay = max(current_delay, STEP_INTERVAL_MIN)

        if not filament_loaded():
            if wait_sensor_clear(current_delay):
                return False

        step_once(current_delay)
    return True

# -------------------------------
# Stepper Run Logic
# -------------------------------
def run_motor():
    """Main motor loop. Ramps up, runs at cruise, exits on stop or runout."""
    delay = SPEED_LEVELS[config["speed_level"]]
    ramp_ok = ramp_motor(delay)
    if not ramp_ok:
        return

    start_time = time.ticks_ms()
    while True:
        if not filament_loaded():
            if wait_sensor_clear(delay):
                return
        if button.value() == 0 and time.ticks_diff(time.ticks_ms(), start_time) > 1000:
            return

        blink_led(led_l if config["direction"] else led_r, 500)
        step_once(delay)

# -------------------------------
# Setup Routine
# -------------------------------
def setup_sequence():
    """Visual startup indication with LED blink and speed selection."""
    clear_leds()
    press_start = None
    level = config["speed_level"]

    for _ in range(6):
        set_led(led_l, LED_BRIGHTNESS if level == 0 else 0)
        set_led(led_r, LED_BRIGHTNESS if level == 2 else 0)
        time.sleep_ms(250)
        clear_leds()
        time.sleep_ms(250)
        if button.value() == 0:
            if press_start is None:
                press_start = time.ticks_ms()
            else:
                if time.ticks_diff(time.ticks_ms(), press_start) > LONG_PRESS_TIME and not filament_loaded():
                    config["direction"] ^= 1  # Toggle direction
                    save_config(config)
                    show_direction()
        else:
            press_start = None
            level = (level + 1) % 3
            config["speed_level"] = level
            save_config(config)

# -------------------------------
# Main Program
# -------------------------------
time.sleep_ms(1000)
en.on()  # Disable motor
dir.value(config["direction"])
setup_sequence()
show_direction()

# Main loop
while True:
    en.on()
    if filament_loaded():
        show_direction()
        if button.value() == 0:
            en.off()
            run_motor()
            show_direction()
    else:
        clear_leds()
