import numpy as np
from roboticstoolbox import RevoluteDH, SerialLink
import matplotlib.pyplot as plt


def CD_Funcion_2R(l1, l2, theta1, theta2):
    q = np.array([theta1, theta2])
    
    robot = SerialLink([
        RevoluteDH(d=0, alpha=0, a=l1, offset=0),
        RevoluteDH(d=0, alpha=0, a=l2, offset=0)
    ], name='HACKER')       

    # Visualizar el robot, con sus limites 
    robot.plot(q, limits= [-25, 25, -25, 25, 0, 5])
    
    MTH = robot.fkine(q)
    return MTH

# Par�metros
l1 = 10
l2 = 10
theta1P1_P2 = 0
theta2P1_P2 = np.linspace(np.pi, 0, 10)

x1y1 = np.zeros((len(theta2P1_P2), 2))

# Iterar sobre theta2P1_P2 y actualizar la animaci�n
for i in range(len(theta2P1_P2)):
    MTH = CD_Funcion_2R(l1, l2, theta1P1_P2, theta2P1_P2[i])
    x1y1[i, 0] = MTH.t[0]
    x1y1[i, 1] = MTH.t[1]
    #plt.gca().set_prop_cycle(None)  #(hold on)    
    # Dibujar un punto en el grafico
    plt.plot(MTH.t[0], MTH.t[1], '*r')

# Mantener la figura abierta
plt.show(block=True)

#plt.gca().set_prop_cycle('auto')  # (hold off)