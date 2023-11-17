#### TIMOTHI ALZUETA - SEPTIEMBRE DE 2023 #####
from ezgame import Ezgame
from point2d import Point2D

from arm import *
#from controllers.incrementer import IncrementerController
from expresion_jacobiana import JacobianController

import time

FPS = 30

# APPLICATION MODES
JACOBIAN = 1  # Cambiar al modo Jacobiano


CURRENT_MODE = JACOBIAN
# Para evitar crear un nuevo Point2D como (0,0) en cada bucle, reutiliza este:
ORIGIN = Point2D()

class Application:
    def __init__(self):
        # Crea una aplicación Ezgame con tamaño (1366x768) y establece su fps en FPS
        self.ez = Ezgame(1366, 768)
        self.ez.fps = FPS
        # self.loop identifica qué función de bucle se utilizará
        self.loop = CURRENT_MODE

        # Para empezar, crea 6 brazos y 6 juntas
        lengths = [100] * 6  # 6 brazos de 100mm cada uno
        thetas = [0, 0, 0, 0, 0, 0]

        # Y los utiliza para crear un brazo
        self.arm = Arm(lengths, thetas)
        self.init()

    def init(self):

        if self.loop == JACOBIAN:
            self.ez.init(self.jacobian_loop)
            self.controller = JacobianController(self.arm)
        else:
            self.exit()

    #######################
    ### COMIENZO BUCLES ###
    #######################

    def incrementer_loop(self):
        # En este modo, dibujamos el brazo
        self.draw_arm(self.arm)
        # Pinta el efector final de azul
        self.ez.point(self.arm.endeffector(), color='blue')
        # Permite que el controlador controle el brazo
        self.controller.control(ORIGIN)

    def jacobian_loop(self):
        # En este modo, dibujamos el brazo
        self.draw_arm(self.arm)
        # Pinta el efector final de azul
        self.ez.point(self.arm.endeffector(), color='blue')
        # Establece la posición del mouse como objetivo
        target = self.ez.getMousePos()
        print(target)
        # Pinta el objetivo de rojo
        self.ez.point(target, color='red')
        # Permite que el controlador controle el brazo
        self.controller.control(target)

    #######################
    ####### FIN BUCLES ####
    #######################

    def draw_arm(self, arm, color='black'):
        # Para dibujar el brazo obtenemos la posición de cada junta
        points = arm.joints_pos()
        for i, p in enumerate(points):
            # Une las juntas con líneas
            if i == 0:
                self.ez.line(ORIGIN, p, color=color)
            else:
                self.ez.line(points[i - 1], p, color=color)
            # Dibuja la junta como un punto
            self.ez.point(p)

    def run(self):
        # Esto solo llama al método run() de ezgame, no te preocupes por eso
        self.ez.run()

    def exit(self):
        exit()


if __name__ == '__main__':
    app = Application()
    app.run()

