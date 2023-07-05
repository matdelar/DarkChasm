import pygame
from random import randint
class ParticleEmitter:
    def __init__(self,screen,speed,color,pos,lifeTime,size,amount = 50,sizeLoss=0,speedLoss=0) -> None:
        self.screen = screen
        self.speed = speed
        self.color = color
        self.emitterPos = [pos[0],pos[1]]
        self.lifeTime = lifeTime
        self.size = size
        self.sizeLoss = sizeLoss
        self.speedLoss = speedLoss
        self.amount = amount
        self.particle = []

        for i in range(self.amount):
            self.particle.append([[self.speed[0]+randint(-3,3),self.speed[1]+randint(-3,3)],self.size,self.emitterPos])
        
        #print(self.particle[0])
        
    def draw(self):
        for i in range(self.amount):
            self.particle[i][2] = self.emitterPos[0]+self.particle[i][2][0]+self.particle[i][0][0],self.emitterPos[1]+self.particle[i][2][1]+self.particle[i][0][1]
            self.particle[i][1] = self.particle[i][1]+randint(0,self.sizeLoss) 
            if self.particle[i][1] <=0:
                self.particle.pop(i)
                self.add()
            pygame.draw.circle(self.screen,self.color,self.particle[i][2],self.particle[i][1])
    
    def add(self):
        self.particle.append([[self.speed[0]+randint(-3,3),self.speed[1]+randint(-3,3)],self.size,self.emitterPos])