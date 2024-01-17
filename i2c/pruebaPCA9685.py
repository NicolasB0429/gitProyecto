#PCA9685
from adafruit_servokit import ServoKit
from time import sleep
kit=ServoKit(channels=16)
servo=16 #Se coloca cuantos canales se van a usar

#Se puede camiar el rango de actuacion del servo
kit.servo[0].set_pulse_width_range(600, 2500)

while True:
    a=input("enter:-")
    kit.servo[0].angle=int(a) #El numero es el canal que se usa