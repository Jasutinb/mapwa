import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

class Decoration(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image_path):
        super().__init__(groups)
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((32, 32))
            self.image.fill('gray')
        self.rect = self.image.get_rect(topleft=pos)

class Door(pygame.sprite.Sprite):
    def __init__(self, pos, groups, target_room, spawn_pos):
        super().__init__(groups)
        self.target_room = target_room
        self.spawn_pos = spawn_pos
        try:
            self.image = pygame.image.load('assets/images/door.png').convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((32, 64))
            self.image.fill('brown')
        self.rect = self.image.get_rect(topleft=pos)

class Bus(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        try:
            self.image = pygame.image.load('assets/images/bus.png').convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((128, 64))
            self.image.fill('yellow')
            pygame.draw.rect(self.image, 'black', (10, 10, 30, 20)) # Window
            pygame.draw.rect(self.image, 'black', (50, 10, 30, 20)) # Window
            pygame.draw.rect(self.image, 'black', (90, 10, 30, 20)) # Window
        self.rect = self.image.get_rect(topleft=pos)
