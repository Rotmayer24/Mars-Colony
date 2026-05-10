import random

class Colonist:
    def __init__(self, habitat):
        self.habitat = habitat
        self.health = 100
        self.x = habitat.x * 64 + random.randint(10, habitat.width * 64 - 10)
        self.y = habitat.y * 64 + random.randint(10, habitat.height * 64 - 10)
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
    
    def get_color(self):
        if self.health > 70:
            return (255, 255, 255)
        elif self.health > 40:
            return (255, 255, 0)
        else:
            return (255, 0, 0)
