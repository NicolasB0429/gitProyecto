import sys
from PyQt5.QtWidgets import QApplication, QWidget
from interfaz import Ui_Form
from clase_robot import Robot

# Crear la aplicacion y el widget
app = QApplication(sys.argv)
Form = QWidget()
ui = Ui_Form()
ui.setupUi(Form)

# Crear una instancia de Robot 
Robot_2R = Robot(nombre="Hacker", l1=10, l2=10, pxInicial=20, pyInicial=0)

# Definir una funcion que llame a Robot_2R.coordenadas con los valores actuales de x e y
def enviar_coordenadas():
    # Obtener los valores de texto de los QTextEdit
    x_str = ui.txt_x.toPlainText()
    y_str = ui.txt_y.toPlainText()

    # Formatear los valores a dos decimales
    x_formateado = "{:.2f}".format(float(x_str))
    y_formateado = "{:.2f}".format(float(y_str))

    # No es necesario convertir los valores formateados nuevamente a n�meros
    x = float(x_formateado)
    y = float(y_formateado)
    Robot_2R.coordenadas(x, y)

# Definir una funcion que llame a Robot_2R.palabra con los caracteres
def enviar_palabra():
    palabra = ui.txt_nombre.toPlainText()
    Robot_2R.palabra(palabra)

# COORDENADAS
ui.btn_1.clicked.connect(enviar_coordenadas)
# ESPACIO DE TRABAJO
ui.btn_2.clicked.connect(Robot_2R.esp_trabajo)
# NOMBRE O CARACTERES
ui.btn_3.clicked.connect(enviar_palabra)
# IMAGENES
# ui.btn_4.clicked.connect(Robot_2R.imagenes(1))
# ui.btn_5.clicked.connect(Robot_2R.imagenes(2))
# ui.btn_6.clicked.connect(Robot_2R.imagenes(3))

# Mostrar el widget y ejecutar la aplicacion
Form.show()
sys.exit(app.exec_())
