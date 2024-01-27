import numpy as np 
import matplotlib.pyplot as plt
from scipy.io import loadmat #Cargar .mat

# Cargar variables desde el archivo .mat
contorno = loadmat('contorno.mat')

# Acceder a las variables cargadas
x1y1 = contorno['x1y1']
x2y2 = contorno['x2y2']
x3y3 = contorno['x3y3']
x4y4 = contorno['x4y4']

#Coordenadas de Usuario
xu = -20
yu = 0

# Banderas
flag1 = 0 #Comparacion seccion derecha
flag2 = 0 #Comparacion seccion izquierda

#Derecha abajo
for i in range(len(x1y1)): 
    if x1y1[i, 0] >= xu:
        if x1y1[i, 1] <= yu:
            print("1. Cumple x y y")
            # print(i)
            flag1 += 1
            break
        else:
            print("1. Solo cumple x")
            # print(i)
            break
    # print(i)

#Derecha arriba
for i in range(len(x2y2)): 
    if x2y2[i, 0] <= xu:
        if x2y2[i, 1] >= yu:
            print("2. Cumple x y y")
            # print(i)
            flag1 += 1
            break
        else:
            print("2. Solo cumple x")
            # print(i)
            break
    # print(i)
        
if flag1 == 2:
    print("Esta dentro del rango de la seccion derecha") 
else:
    print("No Esta dentro del rango de la seccion derecha") 

#Izquierda arriba
for i in range(len(x3y3)): 
    if x3y3[i, 0] <= xu:
        if x3y3[i, 1] >= yu:
            print("3. Cumple x y y")
            # print(i)
            flag2 += 1
            break
        else:
            print("3. Solo cumple x")
            # print(i)
            break
    # print(i)
        
#Izquierda abajo
for i in range(len(x4y4)): 
    if x4y4[i, 0] >= xu:
        if x4y4[i, 1] <= yu:
            print("4. Cumple x y y")
            # print(i)
            flag2 += 1
            break
        else:
            print("4. Solo cumple x")
            # print(i)
            break
    # print(i)
        
if flag2 == 2:
    print("Esta dentro del rango de la seccion izquierda") 
else:
    print("No Esta dentro del rango de la seccion izquierda")