from visual import *
from visual.graph import *

class Ball(object):

    g = 9.80665
    dt=0.01
    t=0

    def __init__(self, initialData, dtt):

        self.vx0 = initialData['vx0']
        self.vy0 = initialData['vy0']
        self.x0 = initialData['x0']
        self.y0 = initialData['y0']
        self.vx = self.vx0
        self.vy = self.vy0
        self.x = self.x0
        self.y = self.y0
        self.R = 1
        self.dt=dtt
        self.nextY = self.y + self.vy * self.dt
        self.mysphere = sphere(pos=vector(self.x0, self.y0, 0), radius=self.R, color=color.red)
        self.velocityVector = arrow(pos=(self.x0, self.y0, 0), axis=(self.vx0, self.vy0, 0), shaftwidth=0.5, color=color.red)

    def nextStep(self):

        self.nextY = self.y + self.vy * self.dt
        if self.nextY > 0:
         self.t += self.dt
         self.vy = self.vy - self.g * self.dt
         self.x = self.x + self.vx * self.dt
         self.y = self.y + self.vy * self.dt
         self.mysphere.pos.x=self.x
         self.mysphere.pos.y=self.y
         self.velocityVector.pos.x=self.x
         self.velocityVector.pos.y=self.y
         self.velocityVector.axis.x=self.vx
         self.velocityVector.axis.y=self.vy
         return True
        else:
         return False





















