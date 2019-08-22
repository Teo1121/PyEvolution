import pygame
import numpy as np
import matplotlib.pyplot as plt
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

    def what(self):
        return player
    
    def update(self,delta):
        self.dir += (2*np.random.random()-1)*np.pi/13

        if self.x-self.sense-self.r/2 < 0 or self.x+self.sense+self.r/2 > WIDTH or self.y-self.sense-self.r/2 < 0 or self.y+self.sense+self.r/2 > HEIGHT:
            self.dir = np.arctan2((-HEIGHT/2+self.y),(WIDTH/2-self.x))        
    
        if self.lookingForFood and len(foods) > 0:
            try:
                closest = min(foods, key=lambda foode:(foode.x-self.x)**2+(foode.y-self.y)**2)
            except:
                return
           
            d = ((closest.x-self.x)**2+(closest.y-self.y)**2)**0.5
            if d < self.r + closest.r:
                oldScore = self.score
                self.score = min(self.score+(closest.nutrients*closest.r*0.15384615384615385),self.foodNeeded)
                closest.update(self.score-oldScore)
                if self.score == self.foodNeeded:
                    self.lookingForFood = False
            elif d-closest.r+min(closest.r/5,5) < self.sense+self.r:
                self.dir = np.arctan2((-closest.y+self.y),(closest.x-self.x))

        
        predator = min(players, key=lambda p:(p.x-self.x)**2+(p.y-self.y)**2 if p != self else 9999999999999999999)
        
        if predator != self and predator.lookingForFood and predator.what() == carnivoir:
            d = ((predator.x-self.x)**2+(predator.y-self.y)**2)**0.5
            if d-predator.r+min(predator.r/5,5) < self.sense+self.r and self.r < predator.r-self.r:
                self.dir = np.arctan2((predator.y-self.y), (-predator.x+self.x))
                
        

            
            
        self.x =min(max(self.x+int(np.cos(self.dir) * self.speed * delta),0),WIDTH)
        self.y =min(max(self.y-int(np.sin(self.dir) * self.speed * delta),0),HEIGHT)        
        
            
    def draw(self):
            pygame.draw.circle(display,(20+int(not self.lookingForFood)*235,min(255*self.speed/2+int(not self.lookingForFood)*255,255),min(255*self.sense/60+int(not self.lookingForFood)*255,255)),(self.x,self.y),int(self.r))
            #pygame.draw.circle(display,(180,180,180),(self.x,self.y),self.r+self.sense,1)

    def reproduce(self,i):
        return player(1+i%3,self.r if np.random.random() < 0.95 else max(self.r+np.random.random()*2-1,1),
                      self.speed if np.random.random() < 0.95 else self.speed+np.random.random()/10-0.05,
                      self.sense if np.random.random() < 0.95 else self.sense+np.random.random()*5-2.5)

    def copy(self,i):
        return player(1+i%3,self.r,self.speed,self.sense)
            
class carnivoir(player):
    
    def what(self):
        return carnivoir
    
    def update(self,delta):
        self.dir += (2*np.random.random()-1)*np.pi/13
        if self.lookingForFood:
            
            if self.x-self.sense-self.r/2 < 0 or self.x+self.sense+self.r/2 > WIDTH or self.y-self.sense-self.r/2 < 0 or self.y+self.sense+self.r/2 > HEIGHT:
                self.dir = np.arctan2((-HEIGHT/2+self.y),(WIDTH/2-self.x))
                
            victim = min(players, key=lambda p:(p.x-self.x)**2+(p.y-self.y)**2 if p != self else 999999999999999999999999999999999999)
            if victim != self and ((victim.what() == carnivoir and victim.lookingForFood) or (victim.what() == player)):
                d = ((victim.x-self.x)**2+(victim.y-self.y)**2)**0.5
                if d-victim.r+min(victim.r/5,5) < self.sense+self.r:
                    if self.r-victim.r >= victim.r:
                        if d < self.r + victim.r:
                            self.score +=  victim.r*0.66666666666
                            players.remove(victim)
                            if self.score >= self.foodNeeded:
                                self.lookingForFood = False
                        else:    
                            self.dir = np.arctan2((-victim.y+self.y),(victim.x-self.x))
                    elif self.r < victim.r-self.r and p.what() == carnivoir:
                        self.dir = np.arctan2((victim.y-self.y), (-victim.x+self.x))

            

            self.x =min(max(self.x+int(np.cos(self.dir) * self.speed * delta),0),WIDTH)
            self.y =min(max(self.y-int(np.sin(self.dir) * self.speed * delta),0),HEIGHT)        

    def draw(self):
            pygame.draw.circle(display,(250,min(200*self.speed/2,210),min(200*self.sense/60,210)),(self.x,self.y),int(self.r))
            #pygame.draw.circle(display,(180,180,180),(self.x,self.y),self.r+self.sense,1)

    def reproduce(self,i):
        return carnivoir(0,self.r if np.random.random() < 0.90 else max(self.r+np.random.random()*2-1,1),
                         self.speed if np.random.random() < 0.90 else self.speed+np.random.random()/10-0.05,
                         self.sense if np.random.random() < 0.90 else self.sense+np.random.random()*5-2.5)
    def copy(self,i):
        return carnivoir(0,self.r if np.random.random() < 0.96 else max(self.r+np.random.random()*2-1,1),
                         self.speed if np.random.random() < 0.96 else self.speed+np.random.random()/10-0.05,
                         self.sense if np.random.random() < 0.96 else self.sense+np.random.random()*5-2.5)
    
def finished(players):
    isThereFood = len(foods) > 0
    for p in players:
        if p.lookingForFood and (p.what() == carnivoir or (isThereFood and p.what() == player)):
            return False
    return True

def textObjects(font,text,color):
    textSureface = font.render(text,True,color)
    return textSureface, textSureface.get_rect()

def message2screen(scr,msg,color = (20,20,20),x=2,y=2,font=sysFont):
    textSurf,textRect = textObjects(font,msg,color)
    textRect.topleft = x, y
    scr.blit(textSurf,textRect)
    
players = []
for i in range(numOfPlayers):
    if i % 5 == 0:
        players.append(carnivoir(0,22,0.7,50))
    else:
        players.append(player(1+i%3,10,0.66666666,80))
        
foods = [food() for i in range(numOfFood)]

game = True

speedAvgP = [0.6666666666666666666666666]
sizeAvgP = [10]
senseAvgP = [80]

speedAvgC = [0.7]
sizeAvgC = [22]
senseAvgC = [50]

last = time.time_ns()
timer = 0

gen = 0
extict = 0
while game and extict < 2:

    now = time.time_ns()
    delta = (now-last)/1000**2
    last = now
    timer += delta
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game = False
                
    if timer >= 3400 or finished(players):
        gen +=1
        t = len(players)
        newPs = []
        numOfPlayers = 0
        extict = 0
        for i in range(t):
            if players[i].score >= players[i].foodNeeded:
                numOfPlayers += 1
                newPs.append(players[i].reproduce(i))
            if players[i].score >= players[i].foodNeeded/2:
                if (players[i].what() == carnivoir and gen%7==0) or (players[i].what() == player):
                    numOfPlayers += 1
                    newPs.append(players[i].copy(i))

        players = newPs
        timer = 0
        foods = [food() for i in range(numOfFood)]
        sumSpeedP = 0
        sumSizeP = 0
        sumSenseP = 0

        sumSpeedC = 0
        sumSizeC = 0
        sumSenseC = 0
        numOfC = 0
        for p in players:
            if p.what() == player:
                sumSpeedP += p.speed
                sumSizeP  += p.r
                sumSenseP += p.sense
            else:
                numOfC += 1
                sumSpeedC += p.speed
                sumSizeC  += p.r
                sumSenseC += p.sense
        try:
            speedAvgP.append(sumSpeedP/(numOfPlayers-numOfC))
            sizeAvgP.append(sumSizeP/(numOfPlayers-numOfC))
            senseAvgP.append(sumSenseP/(numOfPlayers-numOfC))
        except ZeroDivisionError:
            extict += 1
        try:
            speedAvgC.append(sumSpeedC/numOfC)
            sizeAvgC.append(sumSizeC/numOfC)
            senseAvgC.append(sumSenseC/numOfC)
        except ZeroDivisionError:
            extict += 1
    display.fill((51,51,51))
    
    for me in players:  
        me.update(delta)
        me.draw()
    for foode in foods:
        foode.draw()
        
    message2screen(display,"Generation="+str(gen)+
                   ", Population="+str(numOfPlayers)+
                   ", Extinct="+str(extict),(200,200,200))
    
    pygame.display.update()

pygame.quit()

fig, (ax1, ax2, ax3) = plt.subplots(3, 2, sharex=True)
ax1[0].plot(speedAvgP,color='tab:blue')
ax1[1].plot(speedAvgC,color='tab:orange')
ax1[0].set_ylabel('Avrage speed')


ax2[0].plot(sizeAvgP,color='tab:blue')
ax2[1].plot(sizeAvgC,color='tab:orange')
ax2[0].set_ylabel('Avrage size')


ax3[0].plot(senseAvgP,color='tab:blue')
ax3[1].plot(senseAvgC,color='tab:orange')
ax3[0].set_ylabel('Avrage sense')


ax3[0].set_xlabel('Generation')
plt.show()

