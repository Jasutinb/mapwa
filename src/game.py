import pygame
import sys

from src.player import Player
from src.npc import NPC
from src.inventory import Inventory
from src.level import Tile, Decoration, Door

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Student RPG")
        self.clock = pygame.time.Clock()
        self.running = True

        # Sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.floor_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()

        # Level setup
        self.current_room = 'main'
        self.create_map()

        # Player setup
        self.player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), [self.visible_sprites])

        # NPC setup
        self.mom = NPC((SCREEN_WIDTH // 2, 100), [self.visible_sprites], 'assets/images/mom.png', name="Mom")
        self.mom.dialogue = [
            "Hi sweetie!", 
            "Are you ready for your first day at school?", 
            "Don't forget your backpack!",
            "Here's your allowance for today."
        ]

        # Interaction setup
        self.current_dialogue = None
        self.dialogue_index = 0
        self.font = pygame.font.SysFont(None, 24)

        # Inventory setup
        self.inventory = Inventory()

        # Money setup
        self.money = 0
        self.has_talked_to_mom = False

    def create_map(self):
        # Clear existing sprites
        for sprite in self.visible_sprites:
            sprite.kill()
        for sprite in self.floor_sprites:
            sprite.kill()
        for sprite in self.door_sprites:
            sprite.kill()

        if self.current_room == 'main':
            self.create_main_room()
        elif self.current_room == 'bedroom':
            self.create_bedroom()
        elif self.current_room == 'outside':
            self.create_outside()

    def create_main_room(self):
        try:
            floor_surf = pygame.image.load('assets/images/floor.png').convert()
            wall_surf = pygame.image.load('assets/images/wall.png').convert()
        except (pygame.error, FileNotFoundError):
            floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            floor_surf.fill((100, 50, 0))
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill((200, 200, 200))

        # Fill screen with floor tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)
        
        # Add walls at the top
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites], wall_surf)
            Tile((col, TILE_SIZE), [self.visible_sprites], wall_surf)

        # Add a table
        Decoration((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), [self.visible_sprites], 'assets/images/table.png')
        
        # Add doors
        # To Bedroom (left)
        Door((0, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], 'bedroom', (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2))
        # To Outside (right)
        Door((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], 'outside', (64, SCREEN_HEIGHT // 2))

        # Add Mom back if in main room
        if hasattr(self, 'mom'):
            self.visible_sprites.add(self.mom)

    def create_bedroom(self):
        try:
            floor_surf = pygame.image.load('assets/images/floor.png').convert()
            wall_surf = pygame.image.load('assets/images/wall.png').convert()
        except (pygame.error, FileNotFoundError):
            floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            floor_surf.fill((100, 50, 0))
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill((200, 200, 200))

        # Fill screen with floor tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], floor_surf)
        
        # Add walls at the top
        for col in range(0, SCREEN_WIDTH, TILE_SIZE):
            Tile((col, 0), [self.visible_sprites], wall_surf)
            Tile((col, TILE_SIZE), [self.visible_sprites], wall_surf)

        # Add bedroom decorations
        Decoration((100, 100), [self.visible_sprites], 'assets/images/bed.png')
        Decoration((200, 300), [self.visible_sprites], 'assets/images/rug.png')

        # Add door back to Main
        Door((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], 'main', (64, SCREEN_HEIGHT // 2))

    def create_outside(self):
        try:
            grass_surf = pygame.image.load('assets/images/grass.png').convert()
        except (pygame.error, FileNotFoundError):
            grass_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            grass_surf.fill((34, 139, 34))

        # Fill screen with grass tiles
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                Tile((col, row), [self.floor_sprites], grass_surf)

        # Add door back to Main
        Door((0, SCREEN_HEIGHT // 2), [self.visible_sprites, self.door_sprites], 'main', (SCREEN_WIDTH - 64, SCREEN_HEIGHT // 2))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.current_dialogue:
                        # Advance dialogue
                        self.dialogue_index += 1
                        if self.dialogue_index >= len(self.current_dialogue):
                            self.current_dialogue = None
                            self.dialogue_index = 0
                            # Update Mom's dialogue after the first talk
                            if self.has_talked_to_mom:
                                self.mom.dialogue = [
                                    "Hi sweetie!",
                                    "Make sure to study hard!",
                                    "I'll see you later."
                                ]
                        elif not self.has_talked_to_mom and self.dialogue_index == len(self.current_dialogue) - 1:
                            # If it's the last line of the first talk, give money
                            self.money += 250
                            self.has_talked_to_mom = True
                    else:
                        # Try to start interaction
                        if self.check_proximity(self.player, self.mom, 64):
                            self.current_dialogue = self.mom.interact()
                            self.dialogue_index = 0

    def check_proximity(self, sprite1, sprite2, distance):
        p1 = pygame.math.Vector2(sprite1.rect.center)
        p2 = pygame.math.Vector2(sprite2.rect.center)
        return p1.distance_to(p2) < distance

    def update(self):
        if not self.current_dialogue:
            self.visible_sprites.update()
            self.check_transitions()

    def check_transitions(self):
        hits = pygame.sprite.spritecollide(self.player, self.door_sprites, False)
        for door in hits:
            self.current_room = door.target_room
            self.create_map()
            self.player.rect.topleft = door.spawn_pos
            self.visible_sprites.add(self.player)
            break

    def draw(self):
        self.screen.fill((50, 50, 50))  # Dark gray background
        self.floor_sprites.draw(self.screen)
        self.visible_sprites.draw(self.screen)
        
        # Draw proximity hint
        if self.current_room == 'main' and not self.current_dialogue and self.check_proximity(self.player, self.mom, 64):
            hint_surf = self.font.render("Press E to talk", True, 'white')
            hint_rect = hint_surf.get_rect(center=(self.mom.rect.centerx, self.mom.rect.top - 20))
            self.screen.blit(hint_surf, hint_rect)

        # Draw dialogue box
        if self.current_dialogue:
            box_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
            pygame.draw.rect(self.screen, (30, 30, 30), box_rect, border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 200), box_rect, 2, border_radius=10)
            
            text_surf = self.font.render(self.current_dialogue[self.dialogue_index], True, 'white')
            self.screen.blit(text_surf, (box_rect.x + 20, box_rect.y + 20))
            
            prompt_surf = self.font.render("Press E to continue...", True, (150, 150, 150))
            self.screen.blit(prompt_surf, (box_rect.right - 180, box_rect.bottom - 30))

        # Draw money counter
        money_surf = self.font.render(f"Money: ₱{self.money}", True, 'white')
        money_rect = money_surf.get_rect(bottomleft=(20, SCREEN_HEIGHT - 20))
        # Draw a small background for money for better visibility
        bg_rect = money_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (30, 30, 30), bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect, 1, border_radius=5)
        self.screen.blit(money_surf, money_rect)

        self.inventory.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
