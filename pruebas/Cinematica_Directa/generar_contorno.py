import numpy as np 
import matplotlib.pyplot as plt
from scipy.io import savemat #Para guardar .mat
#import roboticstoolbox as rtb

# #Variables globales
# nombre = 'HACKER'
# l1 = 10
# l2 = 10
# can_puntos = 3

# # Derecha Abajo
# theta1P1_P2 = 0
# theta2P1_P2 = np.linspace(np.pi, 0, can_puntos)
# # Inicializar el array x1y1 con ceros
# x1y1 = np.zeros((len(theta2P1_P2), 2))
# # Iterar sobre theta2P1_P2
# for i in range(can_puntos):
#     # Calcular la cinematica directa
#     MTH = CD(l1, l2, theta1P1_P2, theta2P1_P2[i], nombre)
#     # Almacenar las coordenadas x, y en el array x1y1
#     x1y1[i, 0] = MTH.t[0]
#     x1y1[i, 1] = MTH.t[1]
#     #plt.gca().set_prop_cycle(None)  #(hold on)    
#     # Dibujar un punto en el grafico
#     #plt.plot(TH.t[0], MTH.t[1], '*r')

# # Derecha Arriba
# theta1P2_P3 = np.linspace(0, np.pi/2, can_puntos)
# theta2P2_P3 = 0
# # Inicializar el array x1y1 con ceros
# x2y2 = np.zeros((len(theta1P2_P3), 2))
# # Iterar sobre theta2P1_P2
# for i in range(can_puntos):
#     # Calcular la cinematica directa
#     MTH = CD(l1,l2,theta1P2_P3[i], theta2P2_P3, nombre)
#     # Almacenar las coordenadas x, y en el array x1y1
#     x2y2[i, 0] = MTH.t[0]
#     x2y2[i, 1] = MTH.t[1]

# # Izquierda Arriba
# theta1P3_P4 = np.linspace(np.pi/2, np.pi, can_puntos)
# theta2P3_P4 = 0
# # Inicializar el array x1y1 con ceros
# x3y3 = np.zeros((len(theta1P3_P4), 2))
# # Iterar sobre theta2P1_P2
# for i in range(can_puntos):
#     # Calcular la cinematica directa
#     MTH = CD(l1, l2, theta1P3_P4[i], theta2P3_P4, nombre)
#     # Almacenar las coordenadas x, y en el array x1y1
#     x3y3[i, 0] = MTH.t[0]
#     x3y3[i, 1] = MTH.t[1]

# # Izquierda Abajo
# theta1P4_P5 = np.pi
# theta2P4_P5 = np.linspace(0, np.pi, can_puntos)
# # Inicializar el array x1y1 con ceros
# x4y4 = np.zeros((len(theta2P4_P5), 2))
# # Iterar sobre theta2P1_P2
# for i in range(can_puntos):
#     # Calcular la cinematica directa
#     MTH = CD(l1, l2, theta1P4_P5, theta2P4_P5[i], nombre)
#     # Almacenar las coordenadas x, y en el array x1y1
#     x4y4[i, 0] = MTH.t[0]
#     x4y4[i, 1] = MTH.t[1]

# Generar el .mat
# contorno = 'contorno.mat'
# variables = {'x1y1': x1y1, 'x2y2': x2y2, 'x3y3': x3y3, 'x4y4': x4y4}
# savemat(contorno, variables)

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