import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

GRID_SIZE = 64
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100
UI_HEIGHT = 80
BOTTOM_UI_HEIGHT = 50


class Renderer:
    def __init__(self, screen, grid_size=10):
        self.screen = screen
        self.grid_size = grid_size
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 36)
        self.camera = None

    def render(self, game_state, time_scale):
        self.screen.fill(BLACK)
        if game_state.game_over:
            self._render_game_over(game_state)
            return
        self._render_ui(game_state, time_scale)
        self._render_grid()
        self._render_heat(game_state)
        self._render_buildings(game_state)
        self._render_colonists(game_state)
        if game_state.active_event:
            self._render_event(game_state.active_event)

    def _render_ui(self, game_state, time_scale):
        y = 10
        self._render_resource_bar("Power", game_state.power, 50, YELLOW, 50, y)
        self._render_resource_bar(
            "Oxygen", game_state.oxygen, game_state.max_oxygen, (0, 255, 255), 350, y
        )
        self._render_resource_bar(
            "Supplies", game_state.supplies, game_state.max_supplies, GREEN, 650, y
        )
        time_text = f"Time: {game_state.game_time}s"
        time_surface = self.font.render(time_text, True, WHITE)
        self.screen.blit(time_surface, (950, y))
        scale_text = f"Speed: {time_scale}x"
        scale_surface = self.font.render(
            scale_text, True, YELLOW if time_scale < 1.0 else WHITE
        )
        self.screen.blit(scale_surface, (950, y + 30))
        living = len([c for c in game_state.colonists if c.is_alive()])
        colonist_text = f"Colonists: {living}"
        colonist_surface = self.font.render(colonist_text, True, WHITE)
        self.screen.blit(colonist_surface, (1100, y))
        research_hint = "Press R for Research"
        research_surface = self.small_font.render(research_hint, True, GRAY)
        self.screen.blit(research_surface, (1100, y + 30))
        building_hint = "Press 1-5 to build"
        building_surface = self.small_font.render(building_hint, True, GRAY)
        self.screen.blit(building_surface, (50, self.screen.get_height() - 25))
        self._render_tutorial_button()

    def _render_resource_bar(self, label, current, maximum, color, x, y):
        label_surface = self.font.render(label, True, WHITE)
        self.screen.blit(label_surface, (x, y))
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(self.screen, GRAY, (x, y + 25, bar_width, bar_height))
        if maximum > 0:
            fill_width = int((current / maximum) * bar_width)
            fill_width = max(0, min(bar_width, fill_width))
            percentage = current / maximum
            if percentage < 0.25:
                bar_color = RED
            elif percentage < 0.5:
                bar_color = ORANGE
            else:
                bar_color = color
            pygame.draw.rect(
                self.screen, bar_color, (x, y + 25, fill_width, bar_height)
            )
        value_text = f"{int(current)}/{int(maximum)}"
        value_surface = self.small_font.render(value_text, True, WHITE)
        self.screen.blit(value_surface, (x + 5, y + 28))

    def _render_grid(self):
        for x in range(self.grid_size + 1):
            start_x = GRID_OFFSET_X + x * GRID_SIZE
            start_y = GRID_OFFSET_Y
            end_x = GRID_OFFSET_X + x * GRID_SIZE
            end_y = GRID_OFFSET_Y + self.grid_size * GRID_SIZE
            if self.camera:
                start_pos = self.camera.apply(start_x, start_y)
                end_pos = self.camera.apply(end_x, end_y)
            else:
                start_pos = (start_x, start_y)
                end_pos = (end_x, end_y)
            pygame.draw.line(self.screen, GRAY, start_pos, end_pos, 1)
        for y in range(self.grid_size + 1):
            start_x = GRID_OFFSET_X
            start_y = GRID_OFFSET_Y + y * GRID_SIZE
            end_x = GRID_OFFSET_X + self.grid_size * GRID_SIZE
            end_y = GRID_OFFSET_Y + y * GRID_SIZE
            if self.camera:
                start_pos = self.camera.apply(start_x, start_y)
                end_pos = self.camera.apply(end_x, end_y)
            else:
                start_pos = (start_x, start_y)
                end_pos = (end_x, end_y)
            pygame.draw.line(self.screen, GRAY, start_pos, end_pos, 1)

    def _render_heat(self, game_state):
        for tile_x, tile_y in game_state.heated_tiles:
            x = GRID_OFFSET_X + tile_x * GRID_SIZE
            y = GRID_OFFSET_Y + tile_y * GRID_SIZE
            if self.camera:
                screen_x, screen_y = self.camera.apply(x, y)
                size = int(GRID_SIZE * self.camera.zoom)
            else:
                screen_x, screen_y = x, y
                size = GRID_SIZE
            surface = pygame.Surface((size, size))
            surface.set_alpha(30)
            surface.fill(RED)
            self.screen.blit(surface, (screen_x, screen_y))

    def _render_buildings(self, game_state):
        for building in game_state.buildings:
            x = GRID_OFFSET_X + building.x * GRID_SIZE
            y = GRID_OFFSET_Y + building.y * GRID_SIZE
            width = building.width * GRID_SIZE
            height = building.height * GRID_SIZE
            if self.camera:
                screen_x, screen_y = self.camera.apply(x, y)
                screen_width = int(width * self.camera.zoom)
                screen_height = int(height * self.camera.zoom)
            else:
                screen_x, screen_y = x, y
                screen_width, screen_height = width, height
            color = building.color
            if building.power_consumption > 0 and not building.is_powered:
                color = tuple(c // 3 for c in color)
            pygame.draw.rect(
                self.screen,
                color,
                (screen_x + 2, screen_y + 2, screen_width - 4, screen_height - 4),
            )
            pygame.draw.rect(
                self.screen,
                WHITE,
                (screen_x + 2, screen_y + 2, screen_width - 4, screen_height - 4),
                2,
            )
            health_bar_width = screen_width - 8
            health_bar_height = max(4, int(4 * self.camera.zoom)) if self.camera else 4
            health_x = screen_x + 4
            health_y = screen_y + screen_height - 8
            pygame.draw.rect(
                self.screen,
                DARK_GRAY,
                (health_x, health_y, health_bar_width, health_bar_height),
            )
            health_fill = int((building.health / 100) * health_bar_width)
            if building.health > 50:
                health_color = GREEN
            elif building.health > 25:
                health_color = YELLOW
            else:
                health_color = RED
            pygame.draw.rect(
                self.screen,
                health_color,
                (health_x, health_y, health_fill, health_bar_height),
            )
            if game_state.active_event:
                target = game_state.active_event.get_target_building()
                if target == building:
                    if (game_state.game_time % 2) == 0:
                        pygame.draw.rect(
                            self.screen,
                            RED,
                            (screen_x, screen_y, screen_width, screen_height),
                            4,
                        )

    def _render_colonists(self, game_state):
        for colonist in game_state.colonists:
            if colonist.is_alive():
                x = GRID_OFFSET_X + colonist.x
                y = GRID_OFFSET_Y + colonist.y
                if self.camera:
                    screen_x, screen_y = self.camera.apply(x, y)
                    radius = max(2, int(4 * self.camera.zoom))
                else:
                    screen_x, screen_y = x, y
                    radius = 4
                color = colonist.get_color()
                pygame.draw.circle(
                    self.screen, color, (int(screen_x), int(screen_y)), radius
                )

    def _render_event(self, event):
        box_width = 400
        box_height = 80
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = GRID_OFFSET_Y + (self.grid_size * GRID_SIZE) + 55
        pygame.draw.rect(
            self.screen, (100, 0, 0), (box_x, box_y, box_width, box_height)
        )
        pygame.draw.rect(self.screen, RED, (box_x, box_y, box_width, box_height), 3)
        name_surface = self.font.render(event.name, True, WHITE)
        self.screen.blit(name_surface, (box_x + 10, box_y + 10))
        desc_surface = self.small_font.render(event.description, True, WHITE)
        self.screen.blit(desc_surface, (box_x + 10, box_y + 35))
        if event.duration < 999:
            timer_text = f"Time remaining: {event.timer}s"
            timer_surface = self.small_font.render(timer_text, True, YELLOW)
            self.screen.blit(timer_surface, (box_x + 10, box_y + 55))

    def _render_game_over(self, game_state):
        self.screen.fill((20, 0, 0))
        game_over_text = "GAME OVER"
        game_over_surface = self.large_font.render(game_over_text, True, RED)
        text_rect = game_over_surface.get_rect(
            center=(self.screen.get_width() // 2, 200)
        )
        self.screen.blit(game_over_surface, text_rect)
        reason_surface = self.font.render(game_state.game_over_reason, True, WHITE)
        reason_rect = reason_surface.get_rect(
            center=(self.screen.get_width() // 2, 280)
        )
        self.screen.blit(reason_surface, reason_rect)
        time_text = f"Survived: {game_state.game_time} seconds"
        time_surface = self.font.render(time_text, True, YELLOW)
        time_rect = time_surface.get_rect(center=(self.screen.get_width() // 2, 340))
        self.screen.blit(time_surface, time_rect)
        hint_text = "Press ESC to quit"
        hint_surface = self.small_font.render(hint_text, True, GRAY)
        hint_rect = hint_surface.get_rect(center=(self.screen.get_width() // 2, 400))
        self.screen.blit(hint_surface, hint_rect)

    def render_research_panel(self, game_state):
        from research import get_available_research, RESEARCH_TREE

        panel_width = 500
        panel_height = 600
        panel_x = (self.screen.get_width() - panel_width) // 2
        panel_y = (self.screen.get_height() - panel_height) // 2
        pygame.draw.rect(
            self.screen, (20, 20, 40), (panel_x, panel_y, panel_width, panel_height)
        )
        pygame.draw.rect(
            self.screen,
            (100, 100, 255),
            (panel_x, panel_y, panel_width, panel_height),
            3,
        )
        title_surface = self.large_font.render("Research", True, WHITE)
        title_rect = title_surface.get_rect(
            center=(self.screen.get_width() // 2, panel_y + 30)
        )
        self.screen.blit(title_surface, title_rect)
        if game_state.current_research:
            research = RESEARCH_TREE[game_state.current_research]
            progress_text = f"Researching: {research.name}"
            progress_surface = self.font.render(progress_text, True, YELLOW)
            self.screen.blit(progress_surface, (panel_x + 20, panel_y + 70))
            bar_width = panel_width - 40
            bar_height = 20
            bar_x = panel_x + 20
            bar_y = panel_y + 100
            pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
            progress_fill = int(
                (game_state.research_progress / research.duration) * bar_width
            )
            pygame.draw.rect(
                self.screen, GREEN, (bar_x, bar_y, progress_fill, bar_height)
            )
            progress_text = f"{game_state.research_progress}/{research.duration}"
            progress_label = self.small_font.render(progress_text, True, WHITE)
            self.screen.blit(progress_label, (bar_x + 5, bar_y + 3))
        available = get_available_research(game_state.completed_research)
        y_offset = panel_y + 140
        if not available and not game_state.current_research:
            no_research_text = "No research available"
            no_research_surface = self.font.render(no_research_text, True, GRAY)
            self.screen.blit(no_research_surface, (panel_x + 20, y_offset))
        else:
            for research in available:
                button_height = 80
                button_rect = pygame.Rect(
                    panel_x + 20, y_offset, panel_width - 40, button_height
                )
                if game_state.current_research is None:
                    button_color = (40, 40, 80)
                else:
                    button_color = (30, 30, 30)
                pygame.draw.rect(self.screen, button_color, button_rect)
                pygame.draw.rect(self.screen, (80, 80, 160), button_rect, 2)
                name_surface = self.font.render(research.name, True, WHITE)
                self.screen.blit(name_surface, (panel_x + 30, y_offset + 10))
                desc_surface = self.small_font.render(research.description, True, GRAY)
                self.screen.blit(desc_surface, (panel_x + 30, y_offset + 35))
                cost_text = f"Cost: {research.cost} supplies, {research.duration}s"
                cost_surface = self.small_font.render(cost_text, True, YELLOW)
                self.screen.blit(cost_surface, (panel_x + 30, y_offset + 55))
                y_offset += button_height + 10
        close_hint = "Press R or ESC to close"
        close_surface = self.small_font.render(close_hint, True, GRAY)
        close_rect = close_surface.get_rect(
            center=(self.screen.get_width() // 2, panel_y + panel_height - 20)
        )
        self.screen.blit(close_surface, close_rect)

    def _render_tutorial_button(self):
        button_x = 1150
        button_y = 60
        button_width = 100
        button_height = 30
        pygame.draw.rect(
            self.screen,
            (50, 50, 100),
            (button_x, button_y, button_width, button_height),
        )
        pygame.draw.rect(
            self.screen,
            (100, 100, 200),
            (button_x, button_y, button_width, button_height),
            2,
        )
        text_surface = self.small_font.render("Tutorial", True, WHITE)
        text_rect = text_surface.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2)
        )
        self.screen.blit(text_surface, text_rect)

    def _render_building_hotkeys(self, game_state):
        y = GRID_OFFSET_Y + (self.grid_size * GRID_SIZE) + 25
        x_start = GRID_OFFSET_X
        hotkeys = [
            ("1", "power_generator", "Power"),
            ("2", "life_support", "O2"),
            ("3", "greenhouse", "Farm"),
            ("4", "heater", "Heat"),
            ("5", "habitat", "Home"),
        ]
        if "repair_drone" in BUILDING_TYPES:
            req = BUILDING_TYPES["repair_drone"].get("requires_research")
            if req is None or req in game_state.completed_research:
                hotkeys.append(("6", "repair_drone", "Repair"))
        if "battery" in BUILDING_TYPES:
            req = BUILDING_TYPES["battery"].get("requires_research")
            if req is None or req in game_state.completed_research:
                hotkeys.append(("7", "battery", "Battery"))
        for key, building_type, label in hotkeys:
            if building_type in BUILDING_TYPES:
                color = BUILDING_TYPES[building_type]["color"]
                cost = BUILDING_TYPES[building_type]["cost"]
                pygame.draw.rect(self.screen, color, (x_start, y, 20, 20))
                pygame.draw.rect(self.screen, WHITE, (x_start, y, 20, 20), 1)
                key_surface = self.small_font.render(key, True, BLACK)
                self.screen.blit(key_surface, (x_start + 6, y + 3))
                label_text = f"{label} ({cost})"
                label_surface = self.small_font.render(label_text, True, WHITE)
                self.screen.blit(label_surface, (x_start + 25, y + 3))
                x_start += 100
