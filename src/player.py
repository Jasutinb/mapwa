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

        # Animation states
        self.studying = False
        self.study_timer = 0
        self.original_image = self.image.copy()

    def start_study(self, duration_frames):
        self.studying = True
        self.study_timer = duration_frames
        self.direction.xy = (0, 0)

    def input(self):
        if self.studying:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed

    def update(self):
        if self.studying:
            self.study_timer -= 1
            if self.study_timer <= 0:
                self.studying = False
                self.image = self.original_image.copy()
            else:
                # Study animation effect: slight vibration and color pulse
                self.image = self.original_image.copy()
                if (self.study_timer // 5) % 2 == 0:
                    self.image.fill((200, 200, 255), special_flags=pygame.BLEND_RGB_ADD)
                
                # Vibration
                offset_x = (self.study_timer % 3) - 1
                offset_y = ((self.study_timer + 1) % 3) - 1
                self.rect.x += offset_x
                self.rect.y += offset_y
                # Note: we don't need to revert the rect position because move() 
                # or future updates will handle it, or we can just not change rect.
                # Actually, better to just offset the drawing or temporary move.
        
        self.input()
        self.move(self.speed)
