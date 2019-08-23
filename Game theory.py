import numpy as np
import matplotlib.pyplot as plt

numOfGoodies = [50] # identity of Goodies = 1
numOfBadies = [50] # identity of Badies = 3
numOfFoodPairs = 500

playersPos = [0 for i in range(numOfFoodPairs)]
gen = 0

while gen < 500:
    for i in range(numOfBadies[-1]+numOfGoodies[-1]):
        foodPair = np.random.randint(numOfFoodPairs)
        # no more than 2 players on one food pair
        while playersPos[foodPair] == 2 or playersPos[foodPair] == 4 or playersPos[foodPair] == 6: 
            foodPair = foodPair+1 if foodPair+1 != numOfFoodPairs else 0

        player = 1+2*(i%2)
        playersPos[foodPair] += player
        
    tempGoodies = numOfGoodies[-1]
    tempBadies = numOfBadies[-1]
    for i in playersPos:
        if i == 0 or i == 2: # 0 = empty pos, 2 = two Goodies
            continue
        if i == 1: # 1 = one Goodie
            tempGoodies = min(tempGoodies+1,numOfFoodPairs)
        if i == 3: # 3 = one Badie
            tempBadies = min(tempBadies+1,numOfFoodPairs)
        if i == 4: # 4 = one Goodie and one Badie
            tempGoodies = max(tempGoodies-np.random.randint(2),0)
            tempBadies  = min(tempBadies+ np.random.randint(2),numOfFoodPairs)
        if i == 6: # 6 = two Badies
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
