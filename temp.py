from sense_hat import SenseHat
import os
import time

sense = SenseHat()

def get_cpu_temp():
    # Liest die CPU-Temperatur aus
    temp_str = os.popen("vcgencmd measure_temp").readline()
    return float(temp_str.replace("temp=", "").replace("'C\n", ""))

def get_corrected_temp():
    # Rohwert vom Sense HAT
    sense_temp = sense.get_temperature()
    # CPU-Wert
    cpu_temp = get_cpu_temp()
    # Korrektur: Durchschnitt aus Sense-Wert und CPU-Wert, gewichtet
    corrected = sense_temp - ((cpu_temp - sense_temp) / 1.35)
    return round(corrected, 1)

while True:
    temp = get_corrected_temp()
    sense.show_message(f"{temp}C", text_colour=(255, 255, 255), scroll_speed=0.15)
    time.sleep(5)