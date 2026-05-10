import random

class Event:
    def __init__(self, event_type, game_state):
        self.type = event_type
        self.game_state = game_state
        self.duration = EVENT_TYPES[event_type]["duration"]
        self.timer = self.duration
        self.name = EVENT_TYPES[event_type]["name"]
        self.description = EVENT_TYPES[event_type]["description"]
        self._on_start()
    
    def _on_start(self):
        if self.type == "oxygen_leak":
            life_supports = [b for b in self.game_state.buildings 
                           if b.type == "life_support" and b.health > 0]
            if life_supports:
                self.target_building = random.choice(life_supports)
            else:
                self.target_building = None
        elif self.type == "breakdown":
            if self.game_state.buildings:
                self.target_building = random.choice(self.game_state.buildings)
                self.target_building.take_damage(50)
            else:
                self.target_building = None
    
    def update(self):
        self.timer -= 1
        if self.type == "oxygen_leak" and hasattr(self, 'target_building'):
            if self.target_building and self.target_building.health > 0:
                self.game_state.oxygen -= 2
        elif self.type == "dust_storm":
            pass
    
    def is_finished(self):
        return self.timer <= 0
    
    def get_target_building(self):
        if hasattr(self, 'target_building'):
            return self.target_building
        return None

EVENT_TYPES = {
    "dust_storm": {
        "name": "Dust Storm",
        "description": "All buildings take 2x damage",
        "duration": 45,
    },
    "oxygen_leak": {
        "name": "Oxygen Leak",
        "description": "Life support module is leaking oxygen",
        "duration": 999,
    },
    "breakdown": {
        "name": "Equipment Failure",
        "description": "Random building takes heavy damage",
        "duration": 1,
    }
}
