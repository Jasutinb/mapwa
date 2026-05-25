import pygame

class RoomNode:
    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name
        self.left = None
        self.right = None
        self.up = None
        self.down = None

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

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, groups, name, image_path=None):
        super().__init__(groups)
        self.name = name
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
            except (pygame.error, FileNotFoundError):
                self.image = self.create_placeholder()
        else:
            self.image = self.create_placeholder()
        self.rect = self.image.get_rect(topleft=pos)

    def create_placeholder(self):
        surf = pygame.Surface((24, 24))
        surf.fill('cyan')
        pygame.draw.rect(surf, 'white', (4, 4, 16, 16), 2)
        return surf
