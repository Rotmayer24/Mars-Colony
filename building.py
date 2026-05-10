class Building:
    def __init__(self, building_type, x, y):
        self.type = building_type
        self.x = x
        self.y = y
        self.width = BUILDING_TYPES[building_type]["width"]
        self.height = BUILDING_TYPES[building_type]["height"]
        self.health = 100
        self.is_powered = False
        self.is_heated = False
        stats = BUILDING_TYPES[building_type]
        self.power_consumption = stats["power_consumption"]
        self.power_production = stats["power_production"]
        self.output_type = stats.get("output_type", None)
        self.output_amount = stats.get("output_amount", 0)
        self.heat_radius = stats.get("heat_radius", 0)
        self.color = stats["color"]
        self.cost = stats["cost"]

    def is_functional(self):
        if self.health <= 0:
            return False
        if self.power_consumption > 0 and not self.is_powered:
            return False
        if self.type == "greenhouse" and not self.is_heated:
            return False
        return True

    def get_efficiency(self):
        if self.health >= 50:
            return 1.0
        elif self.health >= 25:
            return 0.75
        else:
            return 0.5

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def repair(self, amount):
        self.health = min(100, self.health + amount)

    def occupies_tile(self, tile_x, tile_y):
        return (
            self.x <= tile_x < self.x + self.width
            and self.y <= tile_y < self.y + self.height
        )


BUILDING_TYPES = {
    "power_generator": {
        "name": "Power Generator",
        "width": 2,
        "height": 2,
        "color": (255, 255, 0),
        "power_consumption": 0,
        "power_production": 10,
        "output_type": None,
        "output_amount": 0,
        "heat_radius": 0,
        "cost": 30,
        "description": "Generates 10 power",
        "requires_research": None,
    },
    "life_support": {
        "name": "Life Support",
        "width": 2,
        "height": 2,
        "color": (0, 255, 255),
        "power_consumption": 3,
        "power_production": 0,
        "output_type": "oxygen",
        "output_amount": 5,
        "heat_radius": 0,
        "cost": 40,
        "description": "Consumes 3 power, produces 5 oxygen/tick",
        "requires_research": None,
    },
    "greenhouse": {
        "name": "Greenhouse",
        "width": 2,
        "height": 2,
        "color": (0, 255, 0),
        "power_consumption": 2,
        "power_production": 0,
        "output_type": "supplies",
        "output_amount": 3,
        "heat_radius": 0,
        "cost": 35,
        "description": "Consumes 2 power, produces 3 supplies/tick (needs heat)",
        "requires_research": None,
    },
    "heater": {
        "name": "Heater",
        "width": 1,
        "height": 1,
        "color": (255, 100, 0),
        "power_consumption": 1,
        "power_production": 0,
        "output_type": None,
        "output_amount": 0,
        "heat_radius": 4,
        "cost": 15,
        "description": "Consumes 1 power, heats 4 adjacent tiles",
        "requires_research": None,
    },
    "habitat": {
        "name": "Habitat",
        "width": 3,
        "height": 3,
        "color": (128, 0, 128),
        "power_consumption": 0,
        "power_production": 0,
        "output_type": None,
        "output_amount": 0,
        "heat_radius": 0,
        "cost": 50,
        "description": "Houses 5 colonists",
        "requires_research": None,
    },
    "repair_drone": {
        "name": "Repair Drone",
        "width": 2,
        "height": 2,
        "color": (192, 192, 192),
        "power_consumption": 2,
        "power_production": 0,
        "output_type": "repair",
        "output_amount": 5,
        "heat_radius": 0,
        "cost": 60,
        "description": "Repairs nearby buildings (+5 health every 10 ticks)",
        "requires_research": "auto_repair",
    },
    "battery": {
        "name": "Battery",
        "width": 1,
        "height": 1,
        "color": (255, 215, 0),
        "power_consumption": 0,
        "power_production": 3,
        "output_type": None,
        "output_amount": 0,
        "heat_radius": 0,
        "cost": 40,
        "description": "Provides 3 backup power when needed",
        "requires_research": "backup_power",
    },
}
