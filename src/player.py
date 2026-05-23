import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # Load player image
        try:
            self.image = pygame.image.load('assets/images/player.png').convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Fallback to placeholder if image not found
            self.image = pygame.Surface((32, 64))
            self.image.fill('blue')
        
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 4

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed

    def update(self):
        self.input()
        self.move(self.speed)
