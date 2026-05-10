import pygame
from building import BUILDING_TYPES


class InputHandler:
    def __init__(self, game_state, grid_size=10):
        self.game_state = game_state
        self.grid_size = grid_size
        self.selected_building = None
        self.build_mode = None
        self.time_scale_changed = False
        self.show_research_panel = False
        self.tutorial = None
        self.camera = None
        self.building_hotkeys = {
            pygame.K_1: "power_generator",
            pygame.K_2: "life_support",
            pygame.K_3: "greenhouse",
            pygame.K_4: "heater",
            pygame.K_5: "habitat",
            pygame.K_6: "repair_drone",
            pygame.K_7: "battery",
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event.button, event.pos)

    def _handle_keydown(self, key):
        if key in self.building_hotkeys:
            building_type = self.building_hotkeys[key]
            if building_type in BUILDING_TYPES:
                required_research = BUILDING_TYPES[building_type].get(
                    "requires_research"
                )
                if (
                    required_research
                    and required_research not in self.game_state.completed_research
                ):
                    print(
                        f"Building {building_type} requires research: {required_research}"
                    )
                    self.build_mode = None
                    self.selected_building = None
                    return
                print(f"Selected building: {building_type}")
                self.build_mode = building_type
                self.selected_building = None
        elif key == pygame.K_SPACE:
            self.time_scale_changed = True
        elif key == pygame.K_r:
            self.show_research_panel = not self.show_research_panel
        elif key == pygame.K_ESCAPE:
            if self.show_research_panel:
                self.show_research_panel = False
            elif self.build_mode:
                self.build_mode = None
                self.selected_building = None

    def _handle_mouse_click(self, button, pos):
        if self._check_tutorial_button_click(pos):
            return
        if self.show_research_panel:
            if self._handle_research_click(pos):
                return
        grid_x, grid_y = self._screen_to_grid(pos)
        if grid_x is None:
            return
        if button == 1:
            if self.build_mode:
                self._place_building(grid_x, grid_y)
            else:
                self._select_building(grid_x, grid_y)
        elif button == 3:
            self._repair_building(grid_x, grid_y)

    def _check_tutorial_button_click(self, pos):
        button_rect = pygame.Rect(1150, 60, 100, 30)
        if button_rect.collidepoint(pos):
            if self.tutorial:
                self.tutorial.restart()
            return True
        return False

    def _handle_research_click(self, pos):
        from research import get_available_research

        panel_x = 400
        panel_y = 150
        button_height = 40
        available = get_available_research(self.game_state.completed_research)
        for i, research in enumerate(available):
            button_y = panel_y + 50 + i * (button_height + 10)
            button_rect = pygame.Rect(panel_x + 20, button_y, 400, button_height)
            if button_rect.collidepoint(pos):
                if self.game_state.current_research is None:
                    if self.game_state.start_research(research.id):
                        print(f"Started research: {research.id}")
                        return True
        return False

    def _screen_to_grid(self, pos):
        from renderer import GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE

        x, y = pos
        if self.camera:
            world_x, world_y = self.camera.screen_to_world(x, y)
        else:
            world_x, world_y = x, y
        if (
            world_x < GRID_OFFSET_X
            or world_x >= GRID_OFFSET_X + self.grid_size * GRID_SIZE
            or world_y < GRID_OFFSET_Y
            or world_y >= GRID_OFFSET_Y + self.grid_size * GRID_SIZE
        ):
            return None, None
        grid_x = int((world_x - GRID_OFFSET_X) // GRID_SIZE)
        grid_y = int((world_y - GRID_OFFSET_Y) // GRID_SIZE)
        return grid_x, grid_y

    def _place_building(self, grid_x, grid_y):
        if self.build_mode not in BUILDING_TYPES:
            return
        if self.game_state.place_building(self.build_mode, grid_x, grid_y):
            print(f"Placed {self.build_mode} at ({grid_x}, {grid_y})")
        else:
            print(f"Failed to place {self.build_mode}")

    def _select_building(self, grid_x, grid_y):
        for building in self.game_state.buildings:
            if building.occupies_tile(grid_x, grid_y):
                self.selected_building = building
                return
        self.selected_building = None

    def _repair_building(self, grid_x, grid_y):
        for building in self.game_state.buildings:
            if building.occupies_tile(grid_x, grid_y):
                self.game_state.repair_building(building)
                return
