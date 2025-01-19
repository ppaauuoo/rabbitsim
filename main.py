import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import argparse
from typing import Optional, Any, Dict, List

def rng(func):
    def wrapper(self, *args, **kwargs):
        if random.randrange(2) > 0:
            return
        return func(self, *args, **kwargs)
    return wrapper

class Field:
    def __init__(self,wolfrange:int,rabbitrange:int,grassrange:int):
        self.wolfs = [Wolf() for i in range(wolfrange)]
        self.rabbits = [Rabbit() for i in range(rabbitrange)]
        self.grasses = [Grass() for i in range(grassrange)]
        self.entities = (self.wolfs,self.rabbits)

    def step(self,debug:Optional[bool])->None:
        for entity in self.entities:
            for e in entity:
                e.live()
                self.update(e)
                self.consume(e)
                self.produce(e)
            if debug:
                self.debug(entity)
               
        if len(self.grasses) <= 0 :
            self.grasses.append(Grass())
        self.produce(self.grasses[0])

    @staticmethod
    def debug(entity:object)->None:
        if not entity:
            return
        print('-----Log-----')
        for X in entity:
            print("Type-L-F")
            print(X.name,X.lifespan,X.food)
        print('+++++++++++++')

    def update(self,X:object)->None:
        if not X.dead:
            return
        match X:
            case Rabbit():
                self.rabbits.remove(X)
            case Wolf():
                self.wolfs.remove(X)

    @rng
    def consume(self,X:object)->None:
        if X.food >= X.maxfood:
            return
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
    def produce(self,X:object)->None:
        if isinstance(X,Grass):
            for i in range(X.growth):
                self.grasses.append(Grass())
            return
        if X.food < X.reproducefood or X.age < X.reproduceage:
            return
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
    def __init__(self,name:str,nutrient:int,maxfood:int,metabo:int,reproducefood:int,reproduceage:int,maxage:int,lifespan:int):
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
        
    def live(self)->None:
        self.age +=1
        self.hunger()
        self.die()

    def hunger(self)->None:
        if self.food <=0:
            self.lifespan -= 1
            return
        self.food -= self.metabo
        
    def die(self)->None:
        if self.lifespan <= 0 or self.age >= self.maxage: self.dead = True

class Rabbit(Animal):
    def __init__(self):
        super().__init__("Rabbit",nutrient=10,maxfood=45,metabo=3,reproduceage=10,reproducefood=40,maxage=25,lifespan=3)
    
class Wolf(Animal):
    def __init__(self):
        super().__init__(__class__.__name__,nutrient=10,maxfood=200,metabo=2,reproduceage=10,reproducefood=120,maxage=50,lifespan=2)
    
def main(round:int,seed:Optional[int],logging:Optional[bool],debug:Optional[bool]) -> None:
    if seed is None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    env = Field(2,20,400)
    log = []
    for step in range(round):
        print(f"Round: {step}")
        print(f"Grass:{len(env.grasses)}")
        print(f"Rabbit:{len(env.rabbits)}")
        print(f"Wolf:{len(env.wolfs)}")
        print(f"=============================")
        log.append(dict(Round=step,Grass=len(env.grasses),Rabbit=len(env.rabbits),Wolf=len(env.wolfs)))
        env.step(debug)
    print(f"Seed:{seed}")
    if logging:
        visual(log,seed)


def visual(log:List[Dict],seed:Any) -> None:
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
    parser.add_argument("-r","--round", type=int, default=100, help="Number of Round")
    parser.add_argument("-s","--seed", help="Prefered Seed")
    parser.add_argument("-l","--log", action="store_true", help="Show Chart")
    parser.add_argument("-d","--debug", action="store_true", help="Tracking Lifespan and Hunger of each Object")
    args = parser.parse_args()

    main(args.round,args.seed,args.log,args.debug)
    # rabbit survive : 7495055989988120033

