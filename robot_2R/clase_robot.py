import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH, SerialLink
import matplotlib.pyplot as plt #Para plotear
from scipy.io import loadmat #Cargar .mat
#Servos
from adafruit_servokit import ServoKit
from time import sleep
kit=ServoKit(channels=16)
servo=16 #Se coloca cuantos canales se van a usar
#Se puede cambiar el rango de actuacion del servo
kit.servo[0].set_pulse_width_range(600, 2500)

class robot:
    #Atributos
    def __init__(self, nombre, l1, l2):
        self.nombre = nombre
        self.l1 = l1
        self.l2 = l2
        #Variables globales clase
        self.punto1 = 0
        self.Pxpunto1 = 0
        self.Pypunto1 = 0
    
    def coordenadas(self,xu,yu):
        global punto1, Pxpunto1, Pypunto1
        # Cargar variables desde el archivo .mat
        contorno = loadmat('contorno.mat')
        # Acceder a las variables cargadas
        x1y1 = contorno['x1y1']
        x2y2 = contorno['x2y2']
        x3y3 = contorno['x3y3']
        x4y4 = contorno['x4y4']

        flag1 = 0 #Comparacion seccion derecha
        flag2 = 0 #Comparacion seccion izquierda

        if self.punto1 == 0:
            self.Pxpunto1 = 20
            self.Pypunto1 = 0
            self.punto1 += 1

        [theta1_P1, theta2_P1] = CI(self.l1, self.l2, self.Pxpunto1, self.Pypunto1);

        Px2 = xu
        Py2 = yu

        #Derecha abajo
        for i in range(len(x1y1)): 
            if x1y1[i, 0] >= xu:
                if x1y1[i, 1] <= yu:
                    flag1 += 1
                    break

        #Derecha arriba
        for i in range(len(x2y2)): 
            if x2y2[i, 0] <= xu:
                if x2y2[i, 1] >= yu:
                    flag1 += 1
                    break

        #Izquierda arriba
        for i in range(len(x3y3)): 
            if x3y3[i, 0] <= xu:
                if x3y3[i, 1] >= yu:
                    flag2 += 1
                    break

        #Izquierda abajo
        for i in range(len(x4y4)): 
            if x4y4[i, 0] >= xu:
                if x4y4[i, 1] <= yu:
                    flag2 += 1
                    break
        
        if flag1 == 2 or flag2 == 2:
            [theta1_P2, theta2_P2] = CI(self.l1, self.l2, Px2, Py2)

            theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, 1)
            theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, 1)

            for i in range(len(theta1P1_P2)):
                MTH = CD(self.l1, self.l2, theta1P1_P2[i], theta2P1_P2[i], self.nombre) 
                kit.servo[0].angle= (theta1P1_P2[i]) #Servo 1
                kit.servo[1].angle= (theta2P1_P2[i]) #Servo 2

        else:
            print("No esta dentro del espacio de trabajo del Robot")
            #Aqui va la imagen de error que no esta dentro del espacio de trabajo del Robot
        
        self.Pxpunto1 = Px2
        self.Pypunto1 = Py2

    def esp_trabajo(self):
        can_puntos = 8

        theta1P1_P2 = 0
        theta2P1_P2 = np.linspace((5/6)*np.pi, 0, can_puntos)
        for i in range(len(can_puntos)):
            MTH = CD(self.l1, self.l2, theta1P1_P2, theta2P1_P2[i], self.nombre) 
            kit.servo[0].angle= (theta1P1_P2) #Servo 1
            kit.servo[1].angle= (theta2P1_P2[i]) #Servo 2
            
        theta1P2_P3 = np.linspace(0, np.pi, can_puntos)
        theta2P2_P3 = 0
        for i in range(len(can_puntos)):
            MTH = CD(self.l1, self.l2, theta1P2_P3[i], theta2P2_P3, self.nombre) 
            kit.servo[0].angle= (theta1P2_P3[i]) #Servo 1
            kit.servo[1].angle= (theta2P2_P3) #Servo 2

        theta1P3_P4 = 0
        theta2P3_P4 = np.linspace(0, (5/6)*np.pi, can_puntos)
        for i in range(len(can_puntos)):
            MTH = CD(self.l1, self.l2, theta1P3_P4, theta2P3_P4[i], self.nombre) 
            kit.servo[0].angle= (theta1P3_P4) #Servo 1
            kit.servo[1].angle= (theta2P3_P4[i]) #Servo 2
        
    def palabra(self, palabra):
        print("Prueba")
            

#Cinematica Directa (Angulos a Coordenadas)
def CD(l1, l2, theta1, theta2, nombre):
    q = np.array([theta1, theta2])

    robot = SerialLink([
        RevoluteDH(d=0, alpha=0, a=l1, offset=0),
        RevoluteDH(d=0, alpha=0, a=l2, offset=0)
    ], name= nombre)   
    # Visualizar el robot, con sus limites 
    robot.plot(q, limits= [-25, 25, -25, 25, 0, 5])
    
    MTH = robot.fkine(q)
    return MTH

#Cinematica Inversa (Coordenadas a Angulos)
def CI(l1, l2, px, py):
    b = np.sqrt(px**2 + py**2)
    cos_theta2 = (b**2-l2**2-l1**2)/(2*l2*l1)
    sen_theta2 = np.sqrt(1 - cos_theta2**2)
    theta2 = np.arctan2(sen_theta2, cos_theta2)
    print(f'Theta2 = {np.degrees(theta2):.3f} grados')
    # Calcular alpha y phi para theta1
    alpha = np.arctan2(py,px)
    phi = np.arctan2(l2 * sen_theta2, l1 + l2 * cos_theta2)
    # Calcular theta1
    theta1 = alpha - phi
    theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1 #Otra forma de hacer el if
    print(f'Theta1 = {np.degrees(theta1):.3f} grados')
    #Retorno
    return theta1,theta2
