import pygame
import numpy as np
##import matplotlib.pyplot as plt
import time

WIDTH = 1100
HEIGHT= 800

numOfPlayers = 20
numOfFood = 100

seed = round(time.time())
np.random.seed(seed)
print("The seed is ",seed)

pygame.init()
sysFont = pygame.font.SysFont(None, 30)
display = pygame.display.set_mode((WIDTH,HEIGHT))

class food:
    def __init__(self):
        self.r = 6.5+(np.random.random()*7-3.5)
        self.x = int(self.r*10+(WIDTH- self.r*20)*np.random.random())
        self.y = int(self.r*10+(HEIGHT-self.r*20)*np.random.random())
        self.nutrients = 1.0
    def draw(self):
        pygame.draw.circle(display,(20+235*(1.0-self.nutrients),20+235*self.nutrients,20),(self.x,self.y),int(self.r))
    def update(self,dng):
        self.nutrients -= dng/(self.r*0.15384615384615385)
        if self.nutrients <= 0.001:
            foods.remove(self)
class colony:
    def __init__(self,colony):
        self.r = 50
        self.x = self.r+(WIDTH-self.r*2)*(colony%2)
        self.y = self.r+(HEIGHT-self.r*2)*(colony//3)
        self.color = (255*(colony >> 1 & 1),255*(colony & 1),255*(colony >> 2 & 1))
        self.population = 0
        self.score = 0
    def draw(self):
        pygame.draw.circle(display,self.color,(self.x,self.y),self.r)
        
class player:
    def __init__(self,r,speed,sense,colony):
        
        self.r = r
        self.speed = speed
        self.lookingForFood = True
        self.sense = sense
        
        self.colony = colony
        self.color = colony.color
        colony.population +=1
        
        self.x = colony.x + np.random.randint(-50,50)
        self.y = colony.y + np.random.randint(-50,50)
        
        self.dir = np.arctan2((-HEIGHT/2+self.y),(WIDTH/2-self.x))
        
        self.foodNeeded = (self.r**1.5*self.speed**2+self.speed+(self.sense/8))/8
        #(self.r*self.speed**2+self.speed+(self.sense/10))/5
        self.capacity = 0
        self.storingFood = False
    def update(self,delta):
        self.dir += (2*np.random.random()-1)*np.pi/13

        if self.x-self.sense-self.r/2 < 0 or self.x+self.sense+self.r/2 > WIDTH or self.y-self.sense-self.r/2 < 0 or self.y+self.sense+self.r/2 > HEIGHT:
            self.dir = np.arctan2((-HEIGHT/2+self.y),(WIDTH/2-self.x))        
    
        if len(foods) > 0:
            if self.lookingForFood:
                closest = min(foods, key=lambda foode:(foode.x-self.x)**2+(foode.y-self.y)**2)
                d = ((closest.x-self.x)**2+(closest.y-self.y)**2)**0.5
            
                if d < self.r + closest.r:
                    oldScore = self.capacity
                    self.capacity = min(self.capacity+(closest.nutrients*closest.r*0.15384615384615385),self.foodNeeded)
                    closest.update(self.capacity-oldScore)
                    if self.capacity == self.foodNeeded:
                        self.lookingForFood = False
                        self.storingFood = True
                    
                elif d-closest.r+min(closest.r/5,5) < self.sense+self.r:
                    self.dir = np.arctan2((-closest.y+self.y),(closest.x-self.x))   
        if self.storingFood or (len(foods) == 0 and self.capacity > 0):
                d = ((self.colony.x-self.x)**2+(self.colony.y-self.y)**2)**0.5
                self.dir = np.arctan2((-self.colony.y+self.y),(self.colony.x-self.x))
                if d < self.r + self.colony.r:
                    self.colony.score += self.capacity
                    self.capacity = 0
                    self.storingFood = False
                    self.lookingForFood = True
                
        self.x =min(max(self.x+int(np.cos(self.dir) * self.speed * delta),0),WIDTH)
        self.y =min(max(self.y-int(np.sin(self.dir) * self.speed * delta),0),HEIGHT)        
        
            
    def draw(self):
            pygame.draw.circle(display,self.color,(self.x,self.y),int(self.r))
            #pygame.draw.circle(display,(180,180,180),(self.x,self.y),self.r+self.sense,1)

    def reproduce(self):
        return player(self.r if np.random.random() < 0.95 else max(self.r+np.random.random()*2-1,1),
                      self.speed if np.random.random() < 0.95 else self.speed+np.random.random()/10-0.05,
                      self.sense if np.random.random() < 0.95 else self.sense+np.random.random()*5-2.5,
                      self.colony)

    def copy(self):
        return player(self.r,self.speed,self.sense,self.colony)
            
 
def textObjects(font,text,color):
    textSureface = font.render(text,True,color)
    return textSureface, textSureface.get_rect()

def message2screen(scr,msg,color = (20,20,20),x=2,y=2,font=sysFont):
    textSurf,textRect = textObjects(font,msg,color)
    textRect.topleft = x, y
    scr.blit(textSurf,textRect)

colones = [colony(i) for i in range(1,5)]    
players = [player(10,0.66666,50,colones[i%4]) for i in range(numOfPlayers)]     
foods = [food() for i in range(numOfFood)]

game = True

last = time.time_ns()
timer = 0

gen = 0

while game:

    now = time.time_ns()
    delta = (now-last)/1000**2
    last = now
    
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game = False
                
    if len(foods) == 0:#timer >= 3400 or finished(players):
        timer += delta
        if timer >= 1800:
            gen +=1
            t = len(players)
            newPs = []
            numOfPlayers = 0
            extict = 0
            for i in range(t):
                if players[i].colony.score >= players[i].foodNeeded/2:
                    players[i].colony.score -= players[i].foodNeeded/2
                    numOfPlayers += 1
                    newPs.append(players[i].copy())
                
            for i in range(t):
                if players[i].colony.score >= players[i].foodNeeded:
                    players[i].colony.score -= players[i].foodNeeded
                    numOfPlayers += 1
                    newPs.append(players[i].reproduce())

            players = newPs
            timer = 0
            foods = [food() for i in range(numOfFood)]

    display.fill((51,51,51))
    
    for me in players:  
        me.update(delta)
        me.draw()
    for foode in foods:
        foode.draw()
    for col in colones:
        col.draw()
    message2screen(display,"Generation="+str(gen)+
                   ", Population="+str(numOfPlayers),(200,200,200))
    
    pygame.display.update()

pygame.quit()
