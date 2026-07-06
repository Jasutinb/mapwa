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

class Chair(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (92, 75, 58), (4, 5, 16, 11), border_radius=2)
        pygame.draw.rect(self.image, (125, 102, 76), (5, 2, 14, 5), border_radius=2)
        pygame.draw.rect(self.image, (55, 48, 42), (6, 16, 3, 6))
        pygame.draw.rect(self.image, (55, 48, 42), (15, 16, 3, 6))
        self.rect = self.image.get_rect(topleft=pos)

class ClassMarker(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (36, 86, 148), (4, 5, 24, 22), border_radius=4)
        pygame.draw.rect(self.image, (235, 245, 255), (7, 8, 18, 16), 2, border_radius=2)
        pygame.draw.line(self.image, (235, 245, 255), (10, 13), (22, 13), 2)
        pygame.draw.line(self.image, (235, 245, 255), (10, 18), (20, 18), 2)
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

class PassGate(pygame.sprite.Sprite):
    def __init__(self, pos, groups, target_room, spawn_pos, required_item_id):
        super().__init__(groups)
        self.target_room = target_room
        self.spawn_pos = spawn_pos
        self.required_item_id = required_item_id
        self.image = pygame.Surface((32, 96), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        for x in (4, 14, 24):
            pygame.draw.rect(self.image, (105, 112, 118), (x, 4, 4, 88))
        for y in (12, 42, 72):
            pygame.draw.rect(self.image, (165, 172, 178), (2, y, 28, 4))
        pygame.draw.rect(self.image, (220, 220, 80), (11, 38, 10, 20))
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
    def __init__(self, pos, groups, name, image_path=None, item_id=None):
        super().__init__(groups)
        self.name = name
        self.item_id = item_id or name.lower().replace(" ", "_")
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
