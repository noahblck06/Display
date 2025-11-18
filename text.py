
from sense_hat import SenseHat
from time import sleep


sense = SenseHat()


sense.show_message("hallo mama")


sense.show_message("hallo noah", text_colour=[0,128,0], back_colour=[0,0,128])
#sense.clear()


#temp = sense.get_temperature()
#print("Temperature: %s C" % temp)


#sense.set_imu_config(False,False,True)

#zaehler = 100
#while zaehler > 0:
#   accel_only = sense.get_accelerometer()
#   print("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))
#   zaehler = zaehler -1
#   sleep(0.5)

print("fertig")


















