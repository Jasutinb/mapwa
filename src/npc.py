import pygame
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_path, name="NPC", can_wander=True):
        super().__init__(groups)
        self.name = name
        # Load NPC image
        try:
            self.image = pygame.image.load(sprite_path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Fallback to placeholder if image not found
            self.image = pygame.Surface((32, 64))
            self.image.fill('pink')
        
        self.rect = self.image.get_rect(topleft=pos)
        self.dialogue = [f"Hello, I am {self.name}."]
        self.can_wander = can_wander

        # Movement / Wandering
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.wander_timer = 0
        self.wander_duration = random.randint(60, 120)

    def interact(self):
        return self.dialogue

    def wander(self):
        if self.wander_timer <= 0:
            # Choose a new direction or stay still
            if random.random() < 0.3: # 30% chance to move
                self.direction.x = random.choice([-1, 0, 1])
                self.direction.y = random.choice([-1, 0, 1])
                if self.direction.magnitude() != 0:
                    self.direction = self.direction.normalize()
            else:
                self.direction.x = 0
                self.direction.y = 0
            
            self.wander_timer = self.wander_duration
        else:
            self.wander_timer -= 1

        # Move
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        if self.can_wander:
            self.wander()
