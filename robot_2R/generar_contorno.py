from clase_robot import robot
import numpy as np 
import matplotlib.pyplot as plt
from scipy.io import savemat #Para guardar .mat
#import roboticstoolbox as rtb

#Instancia
robot_2r = robot(nombre="Hacker", l1=10, l2=10)

# # Derecha Abajo
# theta1P1_P2 = 0
# theta2P1_P2 = np.linspace(np.pi, 0, 1000)

# # Inicializar el array x1y1 con ceros
# x1y1 = np.zeros((len(theta2P1_P2), 2))

# # Iterar sobre theta2P1_P2
# for i in range(len(theta2P1_P2)):
#     # Calcular la cinematica directa
#     MTH = robot_2r.CD(theta1P1_P2, theta2P1_P2[i])
#     # Almacenar las coordenadas x, y en el array x1y1
#     x1y1[i, 0] = MTH.t[0]
#     x1y1[i, 1] = MTH.t[1]
#     #plt.gca().set_prop_cycle(None)  #(hold on)    
#     # Dibujar un punto en el grafico
#     #plt.plot(TH.t[0], MTH.t[1], '*r')

# # Derecha Arriba
# theta1P2_P3 = np.linspace(0, np.pi/2, 1000)
# theta2P2_P3 = 0

# # Inicializar el array x1y1 con ceros
# x2y2 = np.zeros((len(theta1P2_P3), 2))

# # Iterar sobre theta2P1_P2
# for i in range(len(theta1P2_P3)):
#     # Calcular la cinematica directa
#     MTH = robot_2r.CD(theta1P2_P3[i], theta2P2_P3)
#     # Almacenar las coordenadas x, y en el array x1y1
#     x2y2[i, 0] = MTH.t[0]
#     x2y2[i, 1] = MTH.t[1]

# # Izquierda Arriba
# theta1P3_P4 = np.linspace(np.pi/2, np.pi, 1000)
# theta2P3_P4 = 0

# # Inicializar el array x1y1 con ceros
# x3y3 = np.zeros((len(theta1P3_P4), 2))

# # Iterar sobre theta2P1_P2
# for i in range(len(theta1P3_P4)):
#     # Calcular la cinematica directa
#     MTH = robot_2r.CD(theta1P3_P4[i], theta2P3_P4)
#     # Almacenar las coordenadas x, y en el array x1y1
#     x3y3[i, 0] = MTH.t[0]
#     x3y3[i, 1] = MTH.t[1]

# # Izquierda Abajo
# theta1P4_P5 = np.pi
# theta2P4_P5 = np.linspace(0, np.pi, 1000)

# # Inicializar el array x1y1 con ceros
# x4y4 = np.zeros((len(theta2P4_P5), 2))

# # Iterar sobre theta2P1_P2
# for i in range(len(theta2P4_P5)):
#     # Calcular la cinematica directa
#     MTH = robot_2r.CD(theta1P4_P5, theta2P4_P5[i])
#     # Almacenar las coordenadas x, y en el array x1y1
#     x4y4[i, 0] = MTH.t[0]
#     x4y4[i, 1] = MTH.t[1]

# contorno = 'contorno.mat'
# variables = {'x1y1': x1y1, 'x2y2': x2y2, 'x3y3': x3y3, 'x4y4': x4y4}
# savemat(contorno, variables)
