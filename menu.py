import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.state = "main"
        self.grid_size_input = 10
        self.custom_input = ""
        self.update_buttons()
        self.hovered_button = None
    
    def update_buttons(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 300
        button_height = 60
        button_x = (screen_width - button_width) // 2
        if self.state == "main":
            self.start_button = pygame.Rect(button_x, screen_height // 2 - 50, button_width, button_height)
            self.settings_button = pygame.Rect(button_x, screen_height // 2 + 30, button_width, button_height)
            self.quit_button = pygame.Rect(button_x, screen_height // 2 + 110, button_width, button_height)
        elif self.state == "settings":
            self.size_10_button = pygame.Rect(button_x, screen_height // 2 - 140, button_width, button_height)
            self.size_15_button = pygame.Rect(button_x, screen_height // 2 - 60, button_width, button_height)
            self.size_20_button = pygame.Rect(button_x, screen_height // 2 + 20, button_width, button_height)
            self.custom_button = pygame.Rect(button_x, screen_height // 2 + 100, button_width, button_height)
            self.back_button = pygame.Rect(button_x, screen_height // 2 + 180, button_width, button_height)
        else:
            self.ok_button = pygame.Rect(button_x, screen_height // 2 + 60, button_width, button_height)
            self.cancel_button = pygame.Rect(button_x, screen_height // 2 + 140, button_width, button_height)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            if self.state == "main":
                if self.start_button.collidepoint(pos):
                    self.hovered_button = "start"
                elif self.settings_button.collidepoint(pos):
                    self.hovered_button = "settings"
                elif self.quit_button.collidepoint(pos):
                    self.hovered_button = "quit"
                else:
                    self.hovered_button = None
            elif self.state == "settings":
                if self.size_10_button.collidepoint(pos):
                    self.hovered_button = "size_10"
                elif self.size_15_button.collidepoint(pos):
                    self.hovered_button = "size_15"
                elif self.size_20_button.collidepoint(pos):
                    self.hovered_button = "size_20"
                elif self.custom_button.collidepoint(pos):
                    self.hovered_button = "custom"
                elif self.back_button.collidepoint(pos):
                    self.hovered_button = "back"
                else:
                    self.hovered_button = None
            else:
                if self.ok_button.collidepoint(pos):
                    self.hovered_button = "ok"
                elif self.cancel_button.collidepoint(pos):
                    self.hovered_button = "cancel"
                else:
                    self.hovered_button = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.state == "main":
                if self.start_button.collidepoint(pos):
                    self.active = False
                    return ("start", self.grid_size_input)
                elif self.settings_button.collidepoint(pos):
                    self.state = "settings"
                    self.update_buttons()
                elif self.quit_button.collidepoint(pos):
                    return ("quit", None)
            elif self.state == "settings":
                if self.size_10_button.collidepoint(pos):
                    self.grid_size_input = 10
                    self.state = "main"
                    self.update_buttons()
                elif self.size_15_button.collidepoint(pos):
                    self.grid_size_input = 15
                    self.state = "main"
                    self.update_buttons()
                elif self.size_20_button.collidepoint(pos):
                    self.grid_size_input = 20
                    self.state = "main"
                    self.update_buttons()
                elif self.custom_button.collidepoint(pos):
                    self.state = "custom"
                    self.custom_input = ""
                    self.update_buttons()
                elif self.back_button.collidepoint(pos):
                    self.state = "main"
                    self.update_buttons()
            else:
                if self.ok_button.collidepoint(pos):
                    if self.custom_input.isdigit():
                        size = int(self.custom_input)
                        if 10 <= size <= 100:
                            self.grid_size_input = size
                            self.state = "main"
                            self.update_buttons()
                elif self.cancel_button.collidepoint(pos):
                    self.state = "settings"
                    self.update_buttons()
        elif event.type == pygame.KEYDOWN:
            if self.state == "custom":
                if event.key == pygame.K_RETURN:
                    if self.custom_input.isdigit():
                        size = int(self.custom_input)
                        if 10 <= size <= 100:
                            self.grid_size_input = size
                            self.state = "main"
                            self.update_buttons()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "settings"
                    self.update_buttons()
                elif event.key == pygame.K_BACKSPACE:
                    self.custom_input = self.custom_input[:-1]
                elif event.unicode.isdigit() and len(self.custom_input) < 3:
                    self.custom_input += event.unicode
            elif event.key == pygame.K_ESCAPE:
                if self.state == "settings":
                    self.state = "main"
                    self.update_buttons()
                else:
                    return ("quit", None)
        return (None, None)
    
    def render(self):
        self.screen.fill((10, 10, 30))
        if self.state == "main":
            self._render_main_menu()
        elif self.state == "settings":
            self._render_settings_menu()
        else:
            self._render_custom_menu()
    
    def _render_main_menu(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 300
        button_height = 60
        button_x = (screen_width - button_width) // 2
        self.start_button = pygame.Rect(button_x, screen_height // 2 - 50, button_width, button_height)
        self.settings_button = pygame.Rect(button_x, screen_height // 2 + 30, button_width, button_height)
        self.quit_button = pygame.Rect(button_x, screen_height // 2 + 110, button_width, button_height)
        title_text = "MARS COLONY"
        title_surface = self.font.render(title_text, True, (255, 50, 50))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 150))
        self.screen.blit(title_surface, title_rect)
        subtitle_text = "Игра на выживание"
        subtitle_surface = self.small_font.render(subtitle_text, True, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(screen_width // 2, 200))
        self.screen.blit(subtitle_surface, subtitle_rect)
        start_color = (50, 100, 50) if self.hovered_button == "start" else (30, 70, 30)
        pygame.draw.rect(self.screen, start_color, self.start_button)
        pygame.draw.rect(self.screen, (100, 200, 100), self.start_button, 3)
        start_text = "Запуск"
        start_surface = self.button_font.render(start_text, True, (255, 255, 255))
        start_text_rect = start_surface.get_rect(center=self.start_button.center)
        self.screen.blit(start_surface, start_text_rect)
        settings_color = (50, 50, 100) if self.hovered_button == "settings" else (30, 30, 70)
        pygame.draw.rect(self.screen, settings_color, self.settings_button)
        pygame.draw.rect(self.screen, (100, 100, 200), self.settings_button, 3)
        settings_text = f"Размер поля: {self.grid_size_input}x{self.grid_size_input}"
        settings_surface = self.button_font.render(settings_text, True, (255, 255, 255))
        settings_text_rect = settings_surface.get_rect(center=self.settings_button.center)
        self.screen.blit(settings_surface, settings_text_rect)
        quit_color = (100, 50, 50) if self.hovered_button == "quit" else (70, 30, 30)
        pygame.draw.rect(self.screen, quit_color, self.quit_button)
        pygame.draw.rect(self.screen, (200, 100, 100), self.quit_button, 3)
        quit_text = "Выход"
        quit_surface = self.button_font.render(quit_text, True, (255, 255, 255))
        quit_text_rect = quit_surface.get_rect(center=self.quit_button.center)
        self.screen.blit(quit_surface, quit_text_rect)
        instructions = [
            "Следите за ресурсами: энергия, кислород, запасы",
            "Стройте здания клавишами 1-5",
            "Исследуйте технологии (клавиша R)",
            "Камера: WASD для движения, колесо мыши для зума"
        ]
        y_offset = screen_height - 150
        for line in instructions:
            text_surface = self.small_font.render(line, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 25
    
    def _render_settings_menu(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 300
        button_height = 60
        button_x = (screen_width - button_width) // 2
        self.size_10_button = pygame.Rect(button_x, screen_height // 2 - 140, button_width, button_height)
        self.size_15_button = pygame.Rect(button_x, screen_height // 2 - 60, button_width, button_height)
        self.size_20_button = pygame.Rect(button_x, screen_height // 2 + 20, button_width, button_height)
        self.custom_button = pygame.Rect(button_x, screen_height // 2 + 100, button_width, button_height)
        self.back_button = pygame.Rect(button_x, screen_height // 2 + 180, button_width, button_height)
        title_text = "РАЗМЕР ПОЛЯ"
        title_surface = self.font.render(title_text, True, (255, 50, 50))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 150))
        self.screen.blit(title_surface, title_rect)
        color_10 = (50, 100, 50) if self.hovered_button == "size_10" else (30, 70, 30)
        pygame.draw.rect(self.screen, color_10, self.size_10_button)
        pygame.draw.rect(self.screen, (100, 200, 100), self.size_10_button, 3)
        text_10 = "10x10 (Маленькое)"
        surface_10 = self.button_font.render(text_10, True, (255, 255, 255))
        rect_10 = surface_10.get_rect(center=self.size_10_button.center)
        self.screen.blit(surface_10, rect_10)
        color_15 = (50, 100, 50) if self.hovered_button == "size_15" else (30, 70, 30)
        pygame.draw.rect(self.screen, color_15, self.size_15_button)
        pygame.draw.rect(self.screen, (100, 200, 100), self.size_15_button, 3)
        text_15 = "15x15 (Среднее)"
        surface_15 = self.button_font.render(text_15, True, (255, 255, 255))
        rect_15 = surface_15.get_rect(center=self.size_15_button.center)
        self.screen.blit(surface_15, rect_15)
        color_20 = (50, 100, 50) if self.hovered_button == "size_20" else (30, 70, 30)
        pygame.draw.rect(self.screen, color_20, self.size_20_button)
        pygame.draw.rect(self.screen, (100, 200, 100), self.size_20_button, 3)
        text_20 = "20x20 (Большое)"
        surface_20 = self.button_font.render(text_20, True, (255, 255, 255))
        rect_20 = surface_20.get_rect(center=self.size_20_button.center)
        self.screen.blit(surface_20, rect_20)
        custom_color = (50, 50, 100) if self.hovered_button == "custom" else (30, 30, 70)
        pygame.draw.rect(self.screen, custom_color, self.custom_button)
        pygame.draw.rect(self.screen, (100, 100, 200), self.custom_button, 3)
        custom_text = "Свой размер"
        custom_surface = self.button_font.render(custom_text, True, (255, 255, 255))
        custom_rect = custom_surface.get_rect(center=self.custom_button.center)
        self.screen.blit(custom_surface, custom_rect)
        back_color = (100, 50, 50) if self.hovered_button == "back" else (70, 30, 30)
        pygame.draw.rect(self.screen, back_color, self.back_button)
        pygame.draw.rect(self.screen, (200, 100, 100), self.back_button, 3)
        back_text = "Назад"
        back_surface = self.button_font.render(back_text, True, (255, 255, 255))
        back_rect = back_surface.get_rect(center=self.back_button.center)
        self.screen.blit(back_surface, back_rect)
    
    def _render_custom_menu(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 300
        button_height = 60
        button_x = (screen_width - button_width) // 2
        self.ok_button = pygame.Rect(button_x, screen_height // 2 + 60, button_width, button_height)
        self.cancel_button = pygame.Rect(button_x, screen_height // 2 + 140, button_width, button_height)
        title_text = "СВОЙ РАЗМЕР"
        title_surface = self.font.render(title_text, True, (255, 50, 50))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 150))
        self.screen.blit(title_surface, title_rect)
        instruction_text = "Введите размер (10-100):"
        instruction_surface = self.small_font.render(instruction_text, True, (200, 200, 200))
        instruction_rect = instruction_surface.get_rect(center=(screen_width // 2, 250))
        self.screen.blit(instruction_surface, instruction_rect)
        input_box = pygame.Rect(button_x, screen_height // 2 - 20, button_width, button_height)
        pygame.draw.rect(self.screen, (50, 50, 50), input_box)
        pygame.draw.rect(self.screen, (100, 100, 200), input_box, 3)
        display_text = self.custom_input if self.custom_input else "10"
        input_surface = self.button_font.render(display_text, True, (255, 255, 255))
        input_rect = input_surface.get_rect(center=input_box.center)
        self.screen.blit(input_surface, input_rect)
        ok_color = (50, 100, 50) if self.hovered_button == "ok" else (30, 70, 30)
        pygame.draw.rect(self.screen, ok_color, self.ok_button)
        pygame.draw.rect(self.screen, (100, 200, 100), self.ok_button, 3)
        ok_text = "OK"
        ok_surface = self.button_font.render(ok_text, True, (255, 255, 255))
        ok_rect = ok_surface.get_rect(center=self.ok_button.center)
        self.screen.blit(ok_surface, ok_rect)
        cancel_color = (100, 50, 50) if self.hovered_button == "cancel" else (70, 30, 30)
        pygame.draw.rect(self.screen, cancel_color, self.cancel_button)
        pygame.draw.rect(self.screen, (200, 100, 100), self.cancel_button, 3)
        cancel_text = "Отмена"
        cancel_surface = self.button_font.render(cancel_text, True, (255, 255, 255))
        cancel_rect = cancel_surface.get_rect(center=self.cancel_button.center)
        self.screen.blit(cancel_surface, cancel_rect)
