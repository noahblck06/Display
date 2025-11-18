from sense_hat import SenseHat
import os
import time
import random

sense = SenseHat()

# Schriftfarbe: Weiß
text_color = (255, 255, 255)

# Scrollgeschwindigkeit und Pause
scroll_speed = 0.15
pause_duration = 0.5

# Teilfaktor zur Temperaturkorrektur
correction_factor = 1.35

# Muster: diagonale Wellenstruktur
pattern_base = [
      [0, 50, 100, 0, 0, 100, 50, 0],
    [100, 150, 200, 100, 100, 200, 150, 100],
    [200, 255, 255, 200, 200, 255, 255, 200],
    [200, 255, 255, 255, 255, 255, 255, 200],
    [150, 200, 255, 255, 255, 255, 200, 150],
    [100, 150, 200, 255, 255, 200, 150, 100],
    [50, 100, 150, 200, 200, 150, 100, 50],
    [0, 50, 100, 150, 150, 100, 50, 0]
]

def get_cpu_temp():
    try:
        temp_str = os.popen("vcgencmd measure_temp").readline()
        return float(temp_str.replace("temp=", "").replace("'C\n", ""))
    except:
        return None

def get_corrected_temp():
    try:
        sense_temp = sense.get_temperature()
        cpu_temp = get_cpu_temp()
        if cpu_temp is None:
            return None
        corrected = sense_temp - ((cpu_temp - sense_temp) / correction_factor)
        return round(corrected, 1)
    except:
        return None

def animate_pattern(cycles=1, delay=0.2):
    for _ in range(cycles):
        pixels = []
        for y in range(8):
            for x in range(8):
                base = pattern_base[y][x]
                flicker = random.randint(-7, 7)
                brightness = max(0, min(255, base + flicker))
                pixels.append((brightness, brightness, brightness))
        sense.set_pixels(pixels)
        time.sleep(delay)

def wait_for_joystick():
    while True:
        events = sense.stick.get_events()
        for event in events:
            if event.action == "pressed":
                return
        animate_pattern(cycles=1)
        time.sleep(0.1)

def check_shutdown():
    events = sense.stick.get_events()
    for event in events:
        if event.direction == "down" and event.action == "pressed":
            os.system("sudo shutdown now")

while True:
    wait_for_joystick()
    temp = get_corrected_temp()
    if temp is not None:
        sense.show_message(f"{temp}C", text_colour=text_color, scroll_speed=scroll_speed)
    time.sleep(pause_duration)