import pygame

class Inventory:
    def __init__(self, slot_count=5, slot_size=64, padding=10):
        self.slot_count = slot_count
        self.slot_size = slot_size
        self.padding = padding
        
        # Calculate bar dimensions
        self.width = (self.slot_size * self.slot_count) + (self.padding * (self.slot_count + 1))
        self.height = self.slot_size + (self.padding * 2)
        
        # Position at bottom center
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        self.rect = pygame.Rect(
            (screen_width - self.width) // 2,
            screen_height - self.height - 20, # 20px margin from bottom
            self.width,
            self.height
        )
        
        self.slots = [None] * self.slot_count # Empty slots

    def add_item(self, item):
        for i in range(self.slot_count):
            if self.slots[i] is None:
                self.slots[i] = item
                return True
        return False

    def draw(self, surface):
        # Draw background bar
        pygame.draw.rect(surface, (40, 40, 40), self.rect, border_radius=10)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2, border_radius=10)
        
        # Draw slots
        for i in range(self.slot_count):
            slot_x = self.rect.x + self.padding + (i * (self.slot_size + self.padding))
            slot_y = self.rect.y + self.padding
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            
            # Draw slot background
            pygame.draw.rect(surface, (60, 60, 60), slot_rect, border_radius=5)
            # Draw slot border
            pygame.draw.rect(surface, (100, 100, 100), slot_rect, 2, border_radius=5)
            
            # Draw item if slot is not empty
            if self.slots[i]:
                # Resize image to fit slot if needed
                item_image = self.slots[i].image
                if item_image.get_width() > self.slot_size - 10 or item_image.get_height() > self.slot_size - 10:
                    item_image = pygame.transform.scale(item_image, (self.slot_size - 10, self.slot_size - 10))
                
                item_rect = item_image.get_rect(center=slot_rect.center)
                surface.blit(item_image, item_rect)
