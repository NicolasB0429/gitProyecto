#PCA9685
from adafruit_servokit import Servokit
from time import sleep
kit=Servokit(chanels=16)
servo=2 #Se coloca cuantos canales se van a usar

while True
    a=input("enter:-")
    kit.servo[2].angle=int(a) #El numero es el canal que se usa