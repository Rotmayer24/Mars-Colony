import pygame
import sys
from game_state import GameState
from renderer import Renderer
from input_handler import InputHandler
from tutorial import Tutorial
from menu import MainMenu
from camera import Camera
from settings import HighScore

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TICK_RATE = 1.0


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mars Colony - Survival Game")
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(self.screen)
        self.highscore = HighScore()
        self.game_state = None
        self.renderer = None
        self.input_handler = None
        self.tutorial = None
        self.grid_size = 10
        self.running = True
        self.in_game = False
        self.tick_timer = 0.0
        self.time_scale = 1.0
        self.paused = False

    def start_game(self, grid_size):
        self.grid_size = grid_size
        self.game_state = GameState(grid_size)
        self.renderer = Renderer(self.screen, grid_size)
        self.input_handler = InputHandler(self.game_state, grid_size)
        self.tutorial = Tutorial()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input_handler.tutorial = self.tutorial
        self.input_handler.camera = self.camera
        self.renderer.camera = self.camera
        self.in_game = True
        self.tick_timer = 0.0
        self.time_scale = 1.0
        self.paused = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    if not self.in_game:
                        action, grid_size = self.menu.handle_event(event)
                        if action == "start":
                            self.start_game(grid_size)
                        elif action == "quit":
                            self.running = False
                    else:
                        if (
                            event.type == pygame.KEYDOWN
                            and event.key == pygame.K_ESCAPE
                        ):
                            if self.game_state.game_over:
                                self.highscore.update(self.game_state.game_time)
                            self.in_game = False
                            self.menu.active = True
                        else:
                            if not self.tutorial.handle_input(event):
                                self.input_handler.handle_event(event)
                        if event.type == pygame.MOUSEWHEEL:
                            self.camera.handle_mouse_wheel(event.y)
            if not self.in_game:
                self.menu.render()
                # Показывать рекорд только в главном меню (не в настройках и не в кастомном вводе)
                if self.menu.state == "main" and self.highscore.best_time > 0:
                    highscore_text = f"Рекорд: {self.highscore.best_time} секунд"
                    font = pygame.font.Font(None, 28)
                    highscore_surface = font.render(highscore_text, True, (255, 215, 0))
                    highscore_rect = highscore_surface.get_rect(
                        center=(SCREEN_WIDTH // 2, 250)
                    )
                    self.screen.blit(highscore_surface, highscore_rect)
            else:
                self.paused = self.tutorial.active
                if not self.paused:
                    keys = pygame.key.get_pressed()
                    self.camera.update(keys)
                    self.tick_timer += dt * self.time_scale
                    if self.tick_timer >= TICK_RATE:
                        self.tick_timer -= TICK_RATE
                        self.game_state.tick()
                    if self.input_handler.time_scale_changed:
                        self.time_scale = 0.5 if self.time_scale == 1.0 else 1.0
                        self.input_handler.time_scale_changed = False
                self.renderer.render(self.game_state, self.time_scale)
                if self.input_handler.show_research_panel:
                    self.renderer.render_research_panel(self.game_state)
                self.tutorial.render(self.screen, self.game_state)
            pygame.display.flip()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
