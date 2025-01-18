import random

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
        self.entities = [self.wolfs,self.rabbits]
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
                        self.grasses.pop()
                case Wolf():
                    if len(self.rabbits) > 0:
                        X.food += X.nutrient
                        X.lifespan = X.maxlifespan
                        self.rabbits.pop()

    @rng
    def produce(self,X):
        if X is None:
            return
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


class Grass(Field):
    def __init__(self):
        self.max = 400
        self.growth = 5
        self.reproduceage = 10
        self.dead = False

class Rabbit(Field):
    def __init__(self):
        self.nutrient = 10
        self.food = 0
        self.maxfood = 45
        self.metabo = 3
        self.reproduceage = 10
        self.reproducefood = 40
        self.age = 0
        self.maxage = 25
        self.lifespan = 3
        self.maxlifespan = 3
        self.dead = False

    def live(self):
        if self.dead:
            return

        self.age +=1
        self.food -= self.metabo
        if self.food <=0:
            self.food = 0
            self.lifespan -= 1
        self.die()


    def die(self):
        if self.food and self.lifespan == 0 or self.age >= self.maxage:
            self.dead = True


class Wolf(Field):
    def __init__(self):
        self.nutrient = 10
        self.food = 0
        self.maxfood = 200
        self.metabo = 2
        self.reproduceage = 10
        self.reproducefood = 120
        self.age = 0
        self.maxage = 50
        self.lifespan = 2
        self.maxlifespan = 2
        self.dead = False

    def live(self):
        if self.dead:
            return

        self.age +=1
        self.food -= self.metabo
        if self.food <=0:
            self.food = 0
            self.lifespan -= 1
        self.die()

    def die(self):
        if self.food and self.lifespan == 0 or self.age >= self.maxage:
            self.dead = True

def main():
    start = 0
    field = Field(1,20,400)
    while start < 100:
        print(f"Round: {start}")
        print(f"Grass:{field.grass}")
        print(f"Rabbit:{field.rabbit}")
        print(f"Wolf:{field.wolf}")
        print(f"=============================")
        field.step()
        start += 1

if __name__ == "__main__":
    main()

