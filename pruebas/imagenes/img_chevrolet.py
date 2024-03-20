import cv2
import numpy as np
import matplotlib.pyplot as plt

#Leer la imagen en formato cv2
imagen = cv2.imread('pruebas/imagenes/img/chevrolet.png')

# Convertir la imagen a escala de grises
img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar suavizado Gaussiano (filtro) Imagen Filtrada
img_fil = cv2.GaussianBlur(img_gris, (5,5), 0) #El 0 calcula la Desviacion Estandar automaticamente

# Encontrar los contornos en la imagen (imagen, metodo, para que se almacenen todos los puntos)
contornos, _ = cv2.findContours(img_fil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(len(contornos)) #Corroborar numero de contornos

# # Visualizar contornos en orden
# for i in range(len(contornos)):
#    #Dibuja (imagen, lista de contronos, indice el contorno (-=todos), color, tamaño)
#     cv2.drawContours(imagen, contornos, i, (0,255,0), 2)
#     cv2.imshow('Imagen', imagen)
#     #Esperar una tecla
#     cv2.waitKey(0)

ofset=500
# COMTORMO #1
# Ajustar espejo, coordenadas y convertirlas en un array numpy
contorno1 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+10.5] for punto in contornos[0]])
# Seleccionar cada n elemento y agregar el ultimo punto
contorno1 = np.vstack([contorno1[0::3], contorno1[-1]])

# COMTORMO #2
# Ajustar espejo, coordenadas y convertirlas en un array numpy
contorno2 = np.array([[(punto[0][0]/100)-10, ((punto[0][1]*-1+ofset)/100)+10.5] for punto in contornos[1]])
# Seleccionar cada n elemento y agregar el ultimo punto
contorno2 = np.vstack([contorno2[0::3], contorno2[-1]])

# Graficar
plt.plot(contorno1[:,0], contorno1[:,1], '*b')
plt.plot(contorno2[:,0], contorno2[:,1], '*b')
plt.grid(True)
plt.show()
