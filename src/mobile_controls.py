import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MobileControls:
    def __init__(self, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        self.screen_width, self.screen_height = screen_size
        self.margin = 24
        self.action_size = 76
        self.joystick_radius = 58
        self.knob_radius = 24
        self.bottom_hud_clearance = 96
        self.dialogue_clearance = 150
        self.dead_zone = 0.18
        self.joystick_center = pygame.math.Vector2(
            self.margin + self.joystick_radius,
            self.screen_height - self.bottom_hud_clearance - self.joystick_radius,
        )
        self.pointer_controls = {}
        self.joystick_pointer = None
        self.joystick_vector = pygame.math.Vector2()
        self.action_down = False
        self.action_pressed = False
        self.menu_down = False
        self.menu_pressed = False
        self.planner_down = False
        self.planner_pressed = False
        self.inventory_slot_pressed = None
        self.inventory_slot_rects = []
        self.font = None
        self.rects = self.create_rects()

    def create_rects(self):
        return {
            "action": pygame.Rect(
                self.screen_width - self.margin - self.action_size,
                self.screen_height - self.dialogue_clearance - self.action_size - self.margin,
                self.action_size,
                self.action_size,
            ),
            "menu": pygame.Rect(
                self.screen_width - self.margin - 92,
                self.screen_height
                - self.dialogue_clearance
                - self.action_size
                - self.margin
                - 60,
                92,
                44,
            ),
            "planner": pygame.Rect(
                self.screen_width - self.margin - 92,
                110,
                92,
                44,
            ),
        }

    @property
    def direction(self):
        return self.joystick_vector.copy()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.press("mouse", event.pos)
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                self.move("mouse", event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.release("mouse")
            elif event.type == pygame.FINGERDOWN:
                self.press(event.finger_id, self.finger_pos(event))
            elif event.type == pygame.FINGERMOTION:
                self.move(event.finger_id, self.finger_pos(event))
            elif event.type == pygame.FINGERUP:
                self.release(event.finger_id)

    def finger_pos(self, event):
        return (
            int(event.x * self.screen_width),
            int(event.y * self.screen_height),
        )

    def press(self, pointer_id, pos):
        control = self.hit_test(pos)
        if not control:
            return

        self.pointer_controls[pointer_id] = control
        if control == "joystick":
            self.joystick_pointer = pointer_id
            self.update_joystick(pos)
        elif control == "action":
            self.action_down = True
            self.action_pressed = True
        elif control == "menu":
            self.menu_down = True
            self.menu_pressed = True
        elif control == "planner":
            self.planner_down = True
            self.planner_pressed = True
        elif control.startswith("inventory_slot:"):
            self.inventory_slot_pressed = int(control.split(":", 1)[1])

    def move(self, pointer_id, pos):
        control = self.pointer_controls.get(pointer_id)
        if control == "joystick":
            self.update_joystick(pos)
        elif control == "action":
            self.action_down = self.rects["action"].collidepoint(pos)
        elif control == "menu":
            self.menu_down = self.rects["menu"].collidepoint(pos)
        elif control == "planner":
            self.planner_down = self.rects["planner"].collidepoint(pos)

    def release(self, pointer_id):
        control = self.pointer_controls.pop(pointer_id, None)
        if not control:
            return

        if control == "joystick" and self.joystick_pointer == pointer_id:
            self.joystick_pointer = None
            self.joystick_vector.xy = (0, 0)
        elif control == "action":
            self.action_down = False
        elif control == "menu":
            self.menu_down = False
        elif control == "planner":
            self.planner_down = False

    def hit_test(self, pos):
        for index, rect in enumerate(self.inventory_slot_rects):
            if rect.collidepoint(pos):
                return f"inventory_slot:{index}"
        if pygame.math.Vector2(pos).distance_to(self.joystick_center) <= (
            self.joystick_radius + self.knob_radius
        ):
            return "joystick"
        if self.rects["action"].collidepoint(pos):
            return "action"
        if self.rects["menu"].collidepoint(pos):
            return "menu"
        if self.rects["planner"].collidepoint(pos):
            return "planner"
        return None

    def set_inventory_slot_rects(self, slot_rects):
        self.inventory_slot_rects = [rect.copy() for rect in slot_rects]

    def update_joystick(self, pos):
        offset = pygame.math.Vector2(pos) - self.joystick_center
        distance = offset.length()
        if distance == 0:
            self.joystick_vector.xy = (0, 0)
            return

        if distance > self.joystick_radius:
            offset = offset.normalize() * self.joystick_radius

        vector = offset / self.joystick_radius
        if vector.length() < self.dead_zone:
            vector.xy = (0, 0)
        self.joystick_vector.xy = vector.xy

    def consume_action_press(self):
        was_pressed = self.action_pressed
        self.action_pressed = False
        return was_pressed

    def consume_menu_press(self):
        was_pressed = self.menu_pressed
        self.menu_pressed = False
        return was_pressed

    def consume_planner_press(self):
        was_pressed = self.planner_pressed
        self.planner_pressed = False
        return was_pressed

    def consume_inventory_slot_press(self):
        slot_index = self.inventory_slot_pressed
        self.inventory_slot_pressed = None
        return slot_index

    def draw(self, screen, planner_only=False):
        if self.font is None:
            try:
                self.font = pygame.font.SysFont("Arial", 22, bold=True)
            except pygame.error:
                self.font = pygame.font.Font(None, 22)

        if not planner_only:
            self.draw_joystick(screen)
            self.draw_action_button(screen)
            self.draw_menu_button(screen)
        self.draw_planner_button(screen)

    def draw_joystick(self, screen):
        base_surface = pygame.Surface(
            (self.joystick_radius * 2, self.joystick_radius * 2), pygame.SRCALPHA
        )
        center = (self.joystick_radius, self.joystick_radius)
        pygame.draw.circle(base_surface, (44, 48, 56, 150), center, self.joystick_radius)
        pygame.draw.circle(
            base_surface,
            (235, 235, 235, 190),
            center,
            self.joystick_radius,
            2,
        )
        base_rect = base_surface.get_rect(center=self.joystick_center)
        screen.blit(base_surface, base_rect)

        knob_center = self.joystick_center + self.joystick_vector * self.joystick_radius
        knob_pos = (round(knob_center.x), round(knob_center.y))
        pygame.draw.circle(screen, (82, 112, 162, 215), knob_pos, self.knob_radius)
        pygame.draw.circle(screen, (255, 255, 255, 220), knob_pos, self.knob_radius, 2)

    def draw_action_button(self, screen):
        rect = self.rects["action"]
        fill = (44, 48, 56, 175) if not self.action_down else (82, 112, 162, 215)
        border = (235, 235, 235, 210)

        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, fill, surface.get_rect(), border_radius=8)
        pygame.draw.rect(surface, border, surface.get_rect(), 2, border_radius=8)

        text_surf = self.font.render("E", True, "white")
        text_rect = text_surf.get_rect(center=surface.get_rect().center)
        surface.blit(text_surf, text_rect)

        screen.blit(surface, rect)

    def draw_menu_button(self, screen):
        rect = self.rects["menu"]
        fill = (44, 48, 56, 175) if not self.menu_down else (82, 112, 162, 215)
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, fill, surface.get_rect(), border_radius=8)
        pygame.draw.rect(surface, (235, 235, 235, 210), surface.get_rect(), 2, border_radius=8)
        text_surf = self.font.render("Menu", True, "white")
        surface.blit(text_surf, text_surf.get_rect(center=surface.get_rect().center))
        screen.blit(surface, rect)

    def draw_planner_button(self, screen):
        rect = self.rects["planner"]
        fill = (44, 48, 56, 175) if not self.planner_down else (82, 112, 162, 215)
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, fill, surface.get_rect(), border_radius=8)
        pygame.draw.rect(surface, (235, 235, 235, 210), surface.get_rect(), 2, border_radius=8)
        text_surf = self.font.render("Planner", True, "white")
        surface.blit(text_surf, text_surf.get_rect(center=surface.get_rect().center))
        screen.blit(surface, rect)
