import random

class Field:
    def __init__(self,wolfrange,rabbitrange,grassrange):
        self.wolfs = [Wolf() for i in wolf]
        self.rabbits = [Rabbit() for i in rabbit]
        self.grasses = [Grass() for i in grass]
        self.wolf = wolfrange
        self.rabbit = rabbitrange
        self.grass = grassrange

    def step(self):
        for w,r,g in zip(self.wolfs, self.rabbits,self.grasses):
            w.live()
            r.live()
            g.live()

            if w.dead:
                self.wolf -= 1
            if r.dead:
                self.rabbit -= 1
            if g.dead:
                self.grass -= 1

class Grass(Field):
    def __init__(self):
        self.max = 400
        self.growth = 5
        self.nutrient = 10
        self.reproduceage = 10

    def live(self):
        offspring()

    def offspring(self):
        super().grasses.push(Grass())

class Rabbit(Field):
    def __init__(self):
        self.nutrient = 10
        self.maxfood = 45
        self.metabo = 3
        self.reproduce = 10

    def live(self):
        self.lifespan -= 1
        if random.randrange(2) > 0:
            self.eat()
        populate()
        die()

    def eat(self):
        if self.food < self.maxfood:
            self.food += 10
            self.lifespan = 2
            super().grasses.push(Grass())

    def die(self):
        if self.food and self.lifespan == 0:
            self.dead = True

    def offspring(self):
        if self.food > 40:
            self.food == 0
            if random.randrange(2) > 0:
                super().rabbits.push(Rabbit())

class Wolf(Field):
    def __init__(self):
        self.maxfood = 200


def main():
    start = 0
    field = Field()
    while start < 10:
        print(f"Grass:{field.grass}")
        print(f"Rabbit:{field.rabbit}")
        print(f"Wolf:{field.wolf}")
        field.grass.live()
        start += 1

if __name__ == "__main__":
    main()

