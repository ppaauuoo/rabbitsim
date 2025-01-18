import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import argparse
from typing import Optional

def rng(func):
    def wrapper(self, *args, **kwargs):
        if random.randrange(2) > 0:
            return
        return func(self, *args, **kwargs)
    return wrapper

class Field:
    def __init__(self,wolfrange,rabbitrange,grassrange):
        self.wolfs = [Wolf() for i in range(wolfrange)]
        self.rabbits = [Rabbit() for i in range(rabbitrange)]
        self.grasses = [Grass() for i in range(grassrange)]
        self.entities = (self.wolfs,self.rabbits)
        self.wolf = wolfrange
        self.rabbit = rabbitrange
        self.grass = grassrange

    def step(self):
        for entity in self.entities:
            for e in entity:
                e.live()
                self.update(e)
                self.consume(e)
                self.produce(e)
                # print('Log')
                # print(e.name,e.lifespan,e.food)
                # print('+++++++++++++++')
                
        self.wolf = len(self.wolfs)
        self.rabbit = len(self.rabbits)
        self.grass = len(self.grasses)

        if len(self.grasses) <= 0 :
            self.grasses.append(Grass())
        self.produce(self.grasses[0])

    def update(self,X):
        if not X.dead:
            return
        match X:
            case Rabbit():
                self.rabbits.remove(X)
            case Wolf():
                self.wolfs.remove(X)

    @rng
    def consume(self,X):
        if isinstance(X,Grass):
            return
        if X.food < X.maxfood:
            match X:
                case Rabbit():
                    if len(self.grasses) > 0:
                        X.food += X.nutrient
                        X.lifespan = X.maxlifespan
                        self.grasses.pop(random.randrange(len(self.grasses)))
                case Wolf():
                    if len(self.rabbits) > 0:
                        X.food += X.nutrient
                        X.lifespan = X.maxlifespan
                        self.rabbits.pop(random.randrange(len(self.rabbits)))

    @rng
    def produce(self,X):
        if isinstance(X,Grass):
            for i in range(X.growth):
                self.grasses.append(Grass())
            return
        if X.food >= X.reproducefood and X.age >= X.reproduceage:
            match X:
                case Rabbit():
                    self.rabbits.append(Rabbit())
                case Wolf():
                    self.wolfs.append(Wolf())


class Grass():
    def __init__(self):
        self.max = 400
        self.growth = 5

class Animal():
    def __init__(self,name,nutrient,maxfood,metabo,reproducefood,reproduceage,maxage,lifespan):
        self.name = name
        self.nutrient = nutrient
        self.food = 0
        self.maxfood = maxfood
        self.metabo = metabo
        self.reproduceage = reproduceage
        self.reproducefood = reproducefood
        self.age = 0
        self.maxage = maxage
        self.lifespan = lifespan
        self.maxlifespan = lifespan
        self.dead = False
        
    def live(self):
        self.age +=1
        self.hunger()
        self.die()

    def hunger(self):
        if self.food <=0:
            self.lifespan -= 1
            return
        self.food -= self.metabo
        
    def die(self):
        if self.lifespan <= 0 or self.age >= self.maxage: self.dead = True

class Rabbit(Animal):
    def __init__(self):
        super().__init__(__name__,nutrient=10,maxfood=45,metabo=3,reproduceage=10,reproducefood=40,maxage=25,lifespan=3)
    
class Wolf(Animal):
    def __init__(self):
        super().__init__(__name__,nutrient=10,maxfood=200,metabo=2,reproduceage=10,reproducefood=120,maxage=50,lifespan=2)
    
def main(round,seed:Optional[int]):
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    env = Field(2,20,400)
    step = 0
    log = []
    while step < round:
        print(f"Round: {step}")
        print(f"Grass:{env.grass}")
        print(f"Rabbit:{env.rabbit}")
        print(f"Wolf:{env.wolf}")
        print(f"=============================")
        
        log.append(dict(Round=step,Grass=len(env.grasses),Rabbit=len(env.rabbits),Wolf=len(env.wolfs)))
        env.step()
        step += 1
    
    print(f"Seed:{seed}")
    data = pd.DataFrame(log)
    
    sns.lineplot(data=data, x='Round', y='Grass', label='Grass')
    sns.lineplot(data=data, x='Round', y='Rabbit', label='Rabbit')
    sns.lineplot(data=data, x='Round', y='Wolf', label='Wolf')
    
    plt.title(f"Seed:{seed}")
    plt.xlabel('Round')
    plt.ylabel('Population')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rabbit and Wolf simulation"
    )
    parser.add_argument("-r","--round", required=False, type=int, default=100, help="Number of Round")
    parser.add_argument("-s","--seed", required=False, type=int, help="Number of Seed")
    args = parser.parse_args()

    main(args.round,args.seed)
    # rabbit survive : 7495055989988120033

