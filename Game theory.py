import numpy as np
import matplotlib.pyplot as plt

numOfGoodies = [50] # 1
numOfBadies = [50] # 4
numOfFoodPairs = 500

playersPos = [0 for i in range(numOfFoodPairs)]
gen = 0

while gen < 500:
    for i in range(numOfBadies[-1]+numOfGoodies[-1]):
        foodPair = np.random.randint(numOfFoodPairs)
        while playersPos[foodPair] == 2 or playersPos[foodPair] == 8 or playersPos[foodPair] == 5:
            foodPair = foodPair+1 if foodPair+1 != numOfFoodPairs else 0

        player = 1+3*(i%2)
        playersPos[foodPair] += player
        
    tempGoodies = numOfGoodies[-1]
    tempBadies = numOfBadies[-1]
    for i in playersPos:
        if i == 0 or i == 2:
            continue
        if i == 1:
            tempGoodies = min(tempGoodies+1,numOfFoodPairs)
        if i == 4:
            tempBadies = min(tempBadies+1,numOfFoodPairs)
        if i == 5:
            tempGoodies = max(tempGoodies-np.random.randint(2),0)
            tempBadies  = min(tempBadies+ np.random.randint(2),numOfFoodPairs)
        if i == 8:
            tempBadies  = max(tempBadies-2,0)
            
           
    numOfGoodies.append(tempGoodies)
    numOfBadies.append(tempBadies)
    playersPos = [0 for i in range(numOfFoodPairs)] 
    gen += 1
    
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.plot(numOfGoodies,color='tab:blue')
ax2.plot(numOfBadies,color='tab:orange')
ax2.set_xlabel('Generation')
ax1.set_ylabel('Population of Goodies')
ax2.set_ylabel('Population of Badies')

plt.show()
