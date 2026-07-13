import pygame

from src.config import MAX_ENERGY, MAX_STRESS, SCREEN_HEIGHT, SCREEN_WIDTH, STATE_PLANNER


class HUDRenderer:
    """Render play HUD state independently from the game loop."""

    _PLANNER_RECTS = (
        "schedule_hud_rect",
        "assignment_hud_rect",
        "exam_hud_rect",
        "grade_hud_rect",
    )
    _URGENT_RECTS = (
        "money_hud_rect",
        "objective_hud_rect",
        "energy_hud_rect",
        "stress_hud_rect",
    )

    def __init__(self, game):
        self.game = game

    def fit_text(self, text, max_width):
        game = self.game
        if game.font.render(text, True, "white").get_width() <= max_width:
            return text

        suffix = "..."
        available = max(
            0,
            max_width - game.font.render(suffix, True, "white").get_width(),
        )
        trimmed = text
        while trimmed and game.font.render(trimmed, True, "white").get_width() > available:
            trimmed = trimmed[:-1]
        return f"{trimmed.rstrip()}{suffix}" if trimmed else suffix

    def draw_text_panel(self, text, text_rect):
        game = self.game
        panel_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(game.screen, (30, 30, 30), panel_rect, border_radius=5)
        pygame.draw.rect(
            game.screen,
            (200, 200, 200),
            panel_rect,
            1,
            border_radius=5,
        )
        game.screen.blit(game.font.render(text, True, "white"), text_rect)
        return panel_rect

    def clear_rects(self, names):
        for name in names:
            setattr(self.game, name, pygame.Rect(0, 0, 0, 0))

    def clear_planner_owned_rects(self):
        self.clear_rects(self._PLANNER_RECTS)

    def clear_urgent_rects(self):
        self.clear_rects(self._URGENT_RECTS)

    def draw(self):
        game = self.game
        self.clear_planner_owned_rects()

        if game.state_machine.current_state_name == STATE_PLANNER:
            self.clear_urgent_rects()
            game.mobile_controls.draw(game.screen, planner_only=True)
            pygame.display.flip()
            return

        energy_text = f"Energy: {game.energy}/{MAX_ENERGY}"
        energy_rect = game.font.render(energy_text, True, "white").get_rect(
            topright=(SCREEN_WIDTH - 25, 20)
        )
        game.energy_hud_rect = self.draw_text_panel(energy_text, energy_rect)

        stress_text = f"Stress: {game.stress}/{MAX_STRESS}"
        stress_rect = game.font.render(stress_text, True, "white").get_rect(
            topright=(SCREEN_WIDTH - 25, game.energy_hud_rect.bottom + 10)
        )
        game.stress_hud_rect = self.draw_text_panel(stress_text, stress_rect)

        objective_max_width = max(160, game.energy_hud_rect.left - 40)
        objective_text = self.fit_text(
            game.get_current_objective_summary(),
            objective_max_width,
        )
        objective_rect = game.font.render(objective_text, True, "white").get_rect(
            topleft=(25, 20)
        )
        game.objective_hud_rect = self.draw_text_panel(objective_text, objective_rect)

        money_text = str(game.money)
        money_surf = game.font.render(money_text, True, "white")
        money_rect = money_surf.get_rect(bottomleft=(60, SCREEN_HEIGHT - 20))
        icon_rect = game.money_icon.get_rect(midleft=(25, money_rect.centery))
        game.money_hud_rect = pygame.Rect(
            15,
            SCREEN_HEIGHT - 45,
            money_surf.get_width() + 55,
            30,
        )
        pygame.draw.rect(
            game.screen,
            (30, 30, 30),
            game.money_hud_rect,
            border_radius=5,
        )
        pygame.draw.rect(
            game.screen,
            (200, 200, 200),
            game.money_hud_rect,
            1,
            border_radius=5,
        )
        game.screen.blit(game.money_icon, icon_rect)
        game.screen.blit(money_surf, money_rect)

        self.draw_location()
        game.inventory.draw(game.screen)
        game.mobile_controls.draw(game.screen)
        pygame.display.flip()

    def draw_location(self):
        game = self.game
        if game.location_display_timer <= 0:
            return

        alpha = min(255, game.location_display_timer * 5)
        try:
            location_font = pygame.font.SysFont("Arial", 48, bold=True)
        except pygame.error:
            location_font = pygame.font.Font(None, 48)
        location_surf = location_font.render(
            game.location_display_text,
            True,
            "white",
        )
        location_surf.set_alpha(alpha)
        location_rect = location_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        shadow_surf = location_font.render(game.location_display_text, True, "black")
        shadow_surf.set_alpha(alpha)
        shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 2, 102))
        game.screen.blit(shadow_surf, shadow_rect)
        game.screen.blit(location_surf, location_rect)
