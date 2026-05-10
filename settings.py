import json
import os

SETTINGS_FILE = "settings.json"
HIGHSCORE_FILE = "highscore.json"

class Settings:
    def __init__(self):
        self.grid_size = 10
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    self.grid_size = data.get('grid_size', 10)
            except:
                pass
    
    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump({'grid_size': self.grid_size}, f)
        except:
            pass

class HighScore:
    def __init__(self):
        self.best_time = 0
        self.load_highscore()
    
    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    self.best_time = data.get('best_time', 0)
            except:
                pass
    
    def save_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'w') as f:
                json.dump({'best_time': self.best_time}, f)
        except:
            pass
    
    def update(self, time):
        if time > self.best_time:
            self.best_time = time
            self.save_highscore()
            return True
        return False
