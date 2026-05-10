import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0
        self.zoom_speed = 0.1
        self.pan_speed = 10
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.pan_speed / self.zoom
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.pan_speed / self.zoom
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.pan_speed / self.zoom
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.pan_speed / self.zoom
    
    def zoom_in(self):
        self.zoom = min(self.max_zoom, self.zoom + self.zoom_speed)
    
    def zoom_out(self):
        self.zoom = max(self.min_zoom, self.zoom - self.zoom_speed)
    
    def handle_mouse_wheel(self, y):
        if y > 0:
            self.zoom_in()
        elif y < 0:
            self.zoom_out()
    
    def apply(self, x, y):
        return (x - self.x) * self.zoom, (y - self.y) * self.zoom
    
    def apply_rect(self, rect):
        x, y = self.apply(rect.x, rect.y)
        width = rect.width * self.zoom
        height = rect.height * self.zoom
        return pygame.Rect(x, y, width, height)
    
    def screen_to_world(self, screen_x, screen_y):
        world_x = (screen_x / self.zoom) + self.x
        world_y = (screen_y / self.zoom) + self.y
        return world_x, world_y
    
    def reset(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
