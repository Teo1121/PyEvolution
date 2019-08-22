import pygame
import numpy as np
import matplotlib.pyplot as plt
import time

WIDTH = 1100
HEIGHT= 800

numOfPlayers = 2
numOfFood = 100

pygame.init()
sysFont = pygame.font.SysFont(None, 30)
display = pygame.display.set_mode((WIDTH,HEIGHT))

class food:
    def __init__(self):
        self.r = 5
        self.x = int(self.r*10+(WIDTH- self.r*20)*np.random.random())
        self.y = int(self.r*10+(HEIGHT-self.r*20)*np.random.random())
        self.nutrients = 1.0
        
    def draw(self):
        pygame.draw.circle(display,(20+235*(1.0-self.nutrients),20+235*self.nutrients,20),(self.x,self.y),self.r)

    def update(self,dng):
        self.nutrients -= dng
        if self.nutrients <= 0:
            foods.remove(self)
        
class player:
    def __init__(self,side,r,speed,sense):
        self.x = int(WIDTH*np.random.random()*abs(np.sin(side*np.pi/2))+WIDTH*(1/(10000*(2-side)**2+1)))
        self.y = int(HEIGHT*np.random.random()*abs(np.cos(side*np.pi/2))+WIDTH*(1/(10000*(1-side)**2+1)))
        
        self.score = 0
        self.dir = np.arctan2((-HEIGHT/2+self.y),(WIDTH/2-self.x))
        self.r = r
        self.speed = speed
        self.lookingForFood = True
        self.sense = sense
        
        self.foodNeeded = (self.r**1.5*self.speed**2+self.speed+(self.sense/8))/8
        #(self.r*self.speed**2+self.speed+(self.sense/10))/5

    def update(self,delta):
        if self.lookingForFood:
            try:
                closest = min(foods, key=lambda foode:(foode.x-self.x)**2+(foode.y-self.y)**2)
            except:
                self.lookingForFood = False
                return
            victim = min(players, key=lambda p:(p.x-self.x)**2+(p.y-self.y)**2 if p != self else 99999999999)
            
            d = ((closest.x-self.x)**2+(closest.y-self.y)**2)**0.5
            if d < self.r + closest.r:
                oldScore = self.score
                self.score = min(self.score+closest.nutrients,self.foodNeeded)
                closest.update(self.score-oldScore)
                if self.score == self.foodNeeded:
                    self.lookingForFood = False
            elif d < self.sense+self.r:
                self.dir = np.arctan2((-closest.y+self.y),(closest.x-self.x))
            elif self.x-self.sense-self.r/2 < 0 or self.x+self.sense+self.r/2 > WIDTH or self.y-self.sense-self.r/2 < 0 or self.y+self.sense+self.r/2 > HEIGHT:
                self.dir = np.arctan2((-HEIGHT/2+self.y),(WIDTH/2-self.x))
            else:
                self.dir += (2*np.random.random()-1)*np.pi/13
            if victim != self and victim.lookingForFood:
                d = ((victim.x-self.x)**2+(victim.y-self.y)**2)**0.5
                if d < self.sense+self.r:
                    if self.r-victim.r >= victim.r:
                        if d < self.r + victim.r:
                            self.score +=  victim.r
                            players.remove(victim)
                            if self.score >= self.foodNeeded:
                                self.lookingForFood = False
                        else:    
                            self.dir = np.arctan2((-victim.y+self.y),(victim.x-self.x))
                    elif self.r < victim.r-self.r:
                        self.dir = np.arctan2((victim.y-self.y), (-victim.x+self.x))
                    
            self.x =min(max(self.x+int(np.cos(self.dir) * self.speed * delta),0),WIDTH)
            self.y =min(max(self.y-int(np.sin(self.dir) * self.speed * delta),0),HEIGHT)        
        
            
    def draw(self):
            pygame.draw.circle(display,(20,min(255*self.speed/2,255),min(255*self.sense/60,255)),(self.x,self.y),int(self.r))
            #pygame.draw.circle(display,(180,180,180),(self.x,self.y),self.r+self.sense,1)

def finished(players):
    for p in players:
        if p.lookingForFood == True:
            return False
    return True

def textObjects(font,text,color):
    textSureface = font.render(text,True,color)
    return textSureface, textSureface.get_rect()

def message2screen(scr,msg,color = (20,20,20),x=2,y=2,font=sysFont):
    textSurf,textRect = textObjects(font,msg,color)
    textRect.topleft = x, y
    scr.blit(textSurf,textRect)
    
players = [player(i%4,10,0.66666666,40) for i in range(numOfPlayers)]
foods = [food() for i in range(numOfFood)]

game = True

speedAvg = [0.6666666666]
sizeAvg = [10]
senseAvg = [40]

last = time.time_ns()
timer = 0

gen = 0
while game:

    now = time.time_ns()
    delta = (now-last)/1000**2
    last = now
    timer += delta
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game = False
                
    if timer >= 800 or finished(players) or len(foods) == 0:
        gen +=1
        t = len(players)
        newPs = []
        numOfPlayers = 0
        for i in range(t):
            if players[i].score == players[i].foodNeeded:
                numOfPlayers += 1
                newPs.append(player(i%4,
                                    players[i].r if np.random.random() < 0.95 else max(players[i].r+np.random.random()*2-1,1),
                                    players[i].speed if np.random.random() < 0.95 else players[i].speed+np.random.random()/10-0.05,
                                    players[i].sense if np.random.random() < 0.95 else players[i].sense+np.random.random()*5-2.5))
            if players[i].score >= players[i].foodNeeded/2:
                numOfPlayers += 1
                newPs.append(player(i%4,players[i].r,players[i].speed,players[i].sense))
        players = newPs
        timer = 0
        foods = [food() for i in range(numOfFood)]
        sumSpeed = 0
        sumSize = 0
        sumSense = 0
        for p in players:
            sumSpeed += p.speed
            sumSize  += p.r
            sumSense += p.sense
        speedAvg.append(sumSpeed/numOfPlayers)
        sizeAvg.append(sumSize/numOfPlayers)
        senseAvg.append(sumSense/numOfPlayers)
        
    display.fill((51,51,51))
    
    for me in players:  
        me.update(delta)
        me.draw()
    for foode in foods:
        foode.draw()
    message2screen(display,str(gen)+", Avrage speed=%.14f"%speedAvg[-1]+
                                    ", Avrage size=%.14f"%sizeAvg[-1]+
                                    ", Avrage sense=%.14f"%senseAvg[-1]+
                                    "  "+str(numOfPlayers),(200,200,200))
    pygame.display.update()
    

pygame.quit()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.plot(speedAvg)
ax1.set_ylabel('Avrage speed')

ax2.plot(sizeAvg)
ax2.set_ylabel('Avrage size')

ax3.plot(senseAvg)
ax3.set_ylabel('Avrage sense')
ax3.set_xlabel('Generation')
plt.show()

