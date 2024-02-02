import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH, SerialLink
import matplotlib.pyplot as plt #Para plotear
from scipy.io import loadmat #Cargar .mat
import cv2 #Para generar contornos imagenes
#Servos
from adafruit_servokit import ServoKit
from time import sleep
kit=ServoKit(channels=16)
servo=16 #Se coloca cuantos canales se van a usar
#Se puede cambiar el rango de actuacion del servo
kit.servo[0].set_pulse_width_range(600, 2500)

class robot:
    #Atributos
    def __init__(self, nombre, l1, l2, pxInicial, pyInicial):
        self.nombre = nombre
        self.l1 = l1
        self.l2 = l2
        #Coordenadas iniciales de cada metodo
        self.pxInicial = pxInicial
        self.pyInicial = pyInicial

    
    def coordenadas(self,xu,yu):
        # Cargar variables desde el archivo .mat
        contorno = loadmat('contorno.mat')
        # Acceder a las variables cargadas
        x1y1 = contorno['x1y1']
        x2y2 = contorno['x2y2']
        x3y3 = contorno['x3y3']
        x4y4 = contorno['x4y4']

        flag1 = 0 #Comparacion seccion derecha
        flag2 = 0 #Comparacion seccion izquierda

        Px1 = self.pxInicial
        Py1 = self.pyInicial
        theta1_P1, theta2_P1 = self.CI(Px1, Py1)

        Px2 = xu
        Py2 = yu
        theta1_P2, theta2_P2 = self.CI(Px2, Py2)

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
            theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, 1)
            theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, 1)

            for i in range(len(theta1P1_P2)):
                # Realizar accion para la ultima iteracion
                if i == len(theta1P1_P2) - 1: #Ultima Iteracion
                    MTH = self.CD(theta1P1_P2[i], theta2P1_P2[i]) 
                    kit.servo[0].angle= (theta1P1_P2[i]) #Servo 1
                    kit.servo[1].angle= (theta2P1_P2[i]) #Servo 2
                    #Guardar ultimas coordenadas, para el siguiente metodo
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                
                # Realizar acci�n para las iteraciones anteriores a la �ltima
                else: 
                    MTH = self.CD(theta1P1_P2[i], theta2P1_P2[i]) 
                    kit.servo[0].angle= (theta1P1_P2[i]) #Servo 1
                    kit.servo[1].angle= (theta2P1_P2[i]) #Servo 2

        else:
            #Aqui va la imagen de error que no esta dentro del espacio de trabajo del Robot
            print("No esta dentro del espacio de trabajo del Robot")
            
    def esp_trabajo(self):
        #Cantidad de linspace y de iteraciones en los for
        can_puntos = 8

        theta1P1_P2 = 0
        theta2P1_P2 = np.linspace((5/6)*np.pi, 0, can_puntos)
        for i in range(len(can_puntos)):
            MTH = self.CD(theta1P1_P2, theta2P1_P2[i]) 
            kit.servo[0].angle= (theta1P1_P2) #Servo 1
            kit.servo[1].angle= (theta2P1_P2[i]) #Servo 2
            
        theta1P2_P3 = np.linspace(0, np.pi, can_puntos)
        theta2P2_P3 = 0
        for i in range(len(can_puntos)):
            MTH = self.CD(theta1P2_P3[i], theta2P2_P3) 
            kit.servo[0].angle= (theta1P2_P3[i]) #Servo 1
            kit.servo[1].angle= (theta2P2_P3) #Servo 2

        theta1P3_P4 = 0
        theta2P3_P4 = np.linspace(0, (5/6)*np.pi, can_puntos)
        for i in range(len(can_puntos)):
            # Realizar accion para la ultima iteracion
            if i == len(can_puntos) - 1: #Ultima Iteracion
                MTH = self.CD(theta1P3_P4, theta2P3_P4[i]) 
                kit.servo[0].angle= (theta1P3_P4) #Servo 1
                kit.servo[1].angle= (theta2P3_P4[i]) #Servo 2
                #Guardar ultimas coordenadas, para el siguiente metodo
                self.pxInicial = MTH.t[0]
                self.pyInicial = MTH.t[1]

            # Realizar accion para las iteraciones anteriores a la ultima
            else: 
                MTH = self.CD(theta1P3_P4, theta2P3_P4[i]) 
                kit.servo[0].angle= (theta1P3_P4) #Servo 1
                kit.servo[1].angle= (theta2P3_P4[i]) #Servo 2
        
    def palabra(self, palabra):
        #Cantidad de puntos para que llegue a coordenadas iniciales para escribir
        can_puntos = 5

        #Punto Iniciales
        Px1 = self.pxInicial
        Py1 = self.pxInicial
        theta1_P1, theta2_P1 = self.CI(Px1, Py1)

        #Coordenadas donde se comienza a escribir
        Px2 = -13
        Py2 = 11
        theta1_P2, theta2_P2 = self.CI(Px2, Py2)

        theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, can_puntos)
        theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, can_puntos)

        for i in range(len(can_puntos)):
            MTH = self.CD(theta1P1_P2[i], theta2P1_P2[i])
            kit.servo[0].angle= (theta1P1_P2[i]) #Servo 1
            kit.servo[1].angle= (theta2P1_P2[i]) #Servo 2

        #Esto es para que se guarden las ultimas coordenadas en pxInicial y pyInicial
        self.pxInicial = Px2
        self.pyInicial = Py2

        if len(palabra)<=9:
            for i in range(len(palabra)):
                Pxf, Pyf = abecedario(palabra[i], self.pxInicial, self.pyInicial)
                self.pxInicial = Pxf
                self.pyInicial = Pyf

        #Cuando la palabra es muu extensa        
        else:
            print("La palabra o nombre excede los 9 caracteres")
        
        #Funciion Interna Para la generacion de letras
        def abecedario(letra, Px, Py):
            #Numero de puntos de todas las letras
            can_puntos = 3
            #IMPORTANTE
            lon = 2 #Esta variable hace lo largo de letra en este caso 2cm

            #Generacion de todas las letras
            if letra == 'a' or letra == 'A':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos) 
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos) 
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)  
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'b' or letra == 'B':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos) 
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos) 
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/1, Px1, Py1, can_puntos)  
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)  
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)     
                 
            elif letra == 'c' or letra == 'C':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon ,Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)

            elif letra == 'd' or letra == 'D':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon + 1, Px1, Py1, can_puntos)

            elif letra == 'e' or letra == 'E':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)

            elif letra == 'f' or letra == 'F':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)

            elif letra == 'g' or letra == 'G':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'h' or letra == 'H':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'i' or letra == 'I':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)

            elif letra == 'j' or letra == 'J':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'k' or letra == 'K':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon, lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                
            elif letra == 'l' or letra == 'L':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                
            elif letra == 'm' or letra == 'M':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, -lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                
            elif letra == 'n' or letra == 'N' or letra == 'ñ' or letra == 'Ñ':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon, -lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                
            elif letra == 'o' or letra == 'O':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)
         
            elif letra == 'p' or letra == 'P':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)     

            elif letra == 'q' or letra == 'Q':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2,lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2,-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'r' or letra == 'R':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2,-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 's' or letra == 's':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 't' or letra == 'T':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon/2, Px1, Py1, can_puntos)
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(-lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                
            elif letra == 'u' or letra == 'U':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'v' or letra == 'V':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, -lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, -lon, Px1, Py1, can_puntos)
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'w' or letra == 'W':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, -lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_vertical(-lon, Px1, Py1, can_puntos)
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'x' or letra == 'X':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_diagonal(lon, lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon, -lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon/2, Px1, Py1, can_puntos)

            elif letra == 'y' or letra == 'Y':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_diagonal(lon, lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(lon/2, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon/2, -lon/2, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)           

            elif letra == 'z' or letra == 'Z':
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_diagonal(lon, lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(-lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_horizontal(lon, Px1, Py1, can_puntos)
                Px1 = Pxf
                Py1 = Pyf
                Pxf, Pyf = linea_diagonal(-lon, -lon, Px1, Py1, can_puntos)
                Px1 = Px
                Py1 = Py
                Pxf, Pyf = linea_horizontal(lon+1, Px1, Py1, can_puntos)

            #Retorno de donde quedan las coordenadas
            return Pxf, Pyf
        
        #Funcion Interna para lineas verticales
        def linea_vertical(lon, Px1, Py1, can_puntos):
            Pxf = Px1
            Pyf = Py1 + lon

            Px7_Pxf = Pxf
            Py7_Pyf = np.linspace(Py1, Pyf, can_puntos)

            for i in range(len(can_puntos)):
                theta1, theta2 = self.CI(Px7_Pxf, Py7_Pyf[i])
                MTH = self.CD(theta1, theta2)
                kit.servo[0].angle= (theta1) #Servo 1
                kit.servo[1].angle= (theta2) #Servo 2
            
            #Retorno
            return Pxf, Pyf
        
        #Funcion Interna para lineas horizontales
        def linea_horizontal(lon, Px1, Py1, can_puntos):
            Pxf = Px1 + lon
            Pyf = Py1 

            Px7_Pxf = np.linspace(Px1, Pxf, can_puntos)
            Py7_Pyf = Pyf

            for i in range(len(can_puntos)):
                theta1, theta2 = self.CI(Px7_Pxf[i], Py7_Pyf)
                MTH = self.CD(theta1, theta2)
                kit.servo[0].angle= (theta1) #Servo 1
                kit.servo[1].angle= (theta2) #Servo 2
            
            #Retorno
            return Pxf, Pyf
        
        #Funcion Interna para lineas horizontales
        def linea_diagonal(lonx, lony, Px1, Py1, can_puntos):
            Pxf = Px1 + lonx
            Pyf = Py1 + lony

            Px7_Pxf = np.linspace(Px1, Pxf, can_puntos)
            Py7_Pyf = np.linspace(Py1, Pyf, can_puntos)

            for i in range(len(can_puntos)):
                theta1, theta2 = self.CI(Px7_Pxf[i], Py7_Pyf[i])
                MTH = self.CD(theta1, theta2)
                kit.servo[0].angle= (theta1) #Servo 1
                kit.servo[1].angle= (theta2) #Servo 2
            
            #Retorno
            return Pxf, Pyf

    def imagenes(self, opcion):
        #FIGURA 1
        if opcion == 1:
            #Leer la imagen en formato cv2
            imagen = cv2.imread('robot_2R/imagenes/hyundai.png')
            # Convertir la imagen a escala de grises
            img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            # Aplicar suavizado Gaussiano (filtro) Imagen Filtrada
            img_fil = cv2.GaussianBlur(img_gris, (5,5), 0) #El 0 calcula la Desviacion Estandar automaticamente
            # Encontrar los contornos en la imagen (imagen, metodo, para que se almacenen todos los puntos)
            contornos, _ = cv2.findContours(img_fil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            ofset=820
            # COMTORMO #1
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno1 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[0]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno1 = np.vstack([contorno1[0::3], contorno1[-1]])

            # COMTORMO #2
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno2 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[1]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno2 = np.vstack([contorno2[0::3], contorno2[-1]])

            # COMTORMO #3
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno3 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[2]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno3 = np.vstack([contorno3[0::3], contorno3[-1]])

            # COMTORMO #4
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno4 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[4]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno4 = np.vstack([contorno4[0::3], contorno4[-1]])

            # COMTORMO #5
            # Ajustar espejo, coordenadas y convertirlas en un array numpy
            contorno5 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+5] for punto in contornos[3]])
            # Seleccionar cada n elemento y agregar el ultimo punto
            contorno5 = np.vstack([contorno5[0::3], contorno5[-1]])

            #CREO QUE ESTO NO IMPORTA (PROBAR)
            # #Puntos iniciales
            # Px1 = self.pxInicial
            # Py1 = self.pyInicial
            # theta1_P1, theta2_P1 = self.CI(Px1, Py1)

            # Px2 = contorno1[-1,0]
            # Py2 = contorno1[-1,1]
            # theta1_P2, theta2_P2 = self.CI(Px2, Py2)

            # theta1P1_P2 = np.linspace(theta1_P1, theta1_P2, 1)
            # theta2P1_P2 = np.linspace(theta2_P1, theta2_P2, 1)

            # for i in range(len(theta1P1_P2)):
            #     MTH = self.CD(theta1P1_P2[i], theta2P1_P2[i]) 
            #     kit.servo[0].angle= (theta1P1_P2[i]) #Servo 1
            #     kit.servo[1].angle= (theta2P1_P2[i]) #Servo 2

            #AHORA SI DIBUJAR CONTORNOS
            #CONTORNO 1
            for i in range(len(contorno1)):
                theta1, theta2 = self.CI(contorno1[i][0],contorno1[i][1])
                MTH = self.CD(theta1, theta2) 
                kit.servo[0].angle= (theta1) #Servo 1
                kit.servo[1].angle= (theta2) #Servo 2

            #CONTORNO 2
            for i in range(len(contorno2)):
                theta1, theta2 = self.CI(contorno2[i][0],contorno2[i][1])
                MTH = self.CD(theta1, theta2) 
                kit.servo[0].angle= (theta1) #Servo 1
                kit.servo[1].angle= (theta2) #Servo 2

            #CONTORNO 3
            for i in range(len(contorno3)):
                theta1, theta2 = self.CI(contorno3[i][0],contorno3[i][1])
                MTH = self.CD(theta1, theta2) 
                kit.servo[0].angle= (theta1) #Servo 1
                kit.servo[1].angle= (theta2) #Servo 2

            #CONTORNO 4
            for i in range(len(contorno4)):
                theta1, theta2 = self.CI(contorno4[i][0],contorno4[i][1])
                MTH = self.CD(theta1, theta2) 
                kit.servo[0].angle= (theta1) #Servo 1
                kit.servo[1].angle= (theta2) #Servo 2

            #CONTORNO 5
            for i in range(len(contorno5)):
                #Ultima Iteracion
                if i == len(contorno5) - 1: 
                    theta1, theta2 = self.CI(contorno5[i][0],contorno5[i][1])
                    MTH = self.CD(theta1, theta2) 
                    kit.servo[0].angle= (theta1) #Servo 1
                    kit.servo[1].angle= (theta2) #Servo 2
                    #Guardar ultimas coordenadas, para el siguiente metodo
                    self.pxInicial = MTH.t[0]
                    self.pyInicial = MTH.t[1]
                # Realizar accion para las iteraciones anteriores a la ultima
                else: 
                    theta1, theta2 = self.CI(contorno5[i][0],contorno5[i][1])
                    MTH = self.CD(theta1, theta2) 
                    kit.servo[0].angle= (theta1) #Servo 1
                    kit.servo[1].angle= (theta2) #Servo 2

        #FIGURA 2
        elif opcion == 2:
            print("Segunda figura")

        #FIGURA 3
        elif opcion == 3:
            print("Tercera figura")

    #Cinematica Directa (Angulos a Coordenadas)
    def CD(self, theta1, theta2):
        q = np.array([theta1, theta2])

        robot = SerialLink([
            RevoluteDH(d=0, alpha=0, a=self.l1, offset=0),
            RevoluteDH(d=0, alpha=0, a=self.l2, offset=0)
        ], name= self.nombre)   
        # Visualizar el robot, con sus limites 
        robot.plot(q, limits= [-25, 25, -25, 25, 0, 5])
        
        MTH = robot.fkine(q)
        return MTH

    #Cinematica Inversa (Coordenadas a Angulos)
    def CI(self, px, py):
        b = np.sqrt(px**2 + py**2)
        cos_theta2 = (b**2-self.l2**2-self.l1**2)/(2*self.l2*self.l1)
        sen_theta2 = np.sqrt(1 - cos_theta2**2)
        theta2 = np.arctan2(sen_theta2, cos_theta2)
        print(f'Theta2 = {np.degrees(theta2):.3f} grados')
        # Calcular alpha y phi para theta1
        alpha = np.arctan2(py,px)
        phi = np.arctan2(self.l2 * sen_theta2, self.l1 + self.l2 * cos_theta2)
        # Calcular theta1
        theta1 = alpha - phi
        theta1 = theta1 + 2 * np.pi if theta1 <= -np.pi else theta1 #Otra forma de hacer el if
        print(f'Theta1 = {np.degrees(theta1):.3f} grados')
        #Retorno
        return theta1,theta2
