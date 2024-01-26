import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH, SerialLink
import matplotlib.pyplot as plt

class robot:
    #Atributos
    def __init__(self, nombre, l1, l2):
        self.nombre = nombre
        self.l1 = l1
        self.l2 = l2

    #METODOS    
    #Cinematica Directa (Angulos a coordenadas)
    def CD(self, theta1, theta2):
        q = np.array([theta1, theta2])
    
        robot = SerialLink([
            RevoluteDH(d=0, alpha=0, a=self.l1, offset=0),
            RevoluteDH(d=0, alpha=0, a=self.l2, offset=0)
        ], name='HACKER')   

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
