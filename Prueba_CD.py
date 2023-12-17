import numpy as np
import roboticstoolbox as rtb

# Definir los ángulos theta1 y theta2
theta1 = 0
theta2 = 90

# Crear el vector de configuración q
q = np.array([theta1, theta2])

# Definir longitudes de los eslabones
l1 = 10
l2 = 10

# Definir la cadena cinemática
R = [
    rtb.RevoluteDH(d=0, alpha=0, a=l1, offset=0),
    rtb.RevoluteDH(d=0, alpha=0, a=l2, offset=0)
]

# Crear el robot serial
Robot = rtb.DHRobot(R, name='Hola')
print(Robot)

# Graficar el robot
Robot.teach(q,limits=[-25, 25, -15, 25, -30, 30])
# ylim([10 20])
#zlim([-10, 10])


