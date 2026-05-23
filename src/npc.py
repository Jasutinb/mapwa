import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_path, name="NPC"):
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

    def interact(self):
        return self.dialogue

    def update(self):
        # NPCs could have movement or interaction logic here later
        pass
