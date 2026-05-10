import random
from building import Building, BUILDING_TYPES
from colonist import Colonist
from events import Event, EVENT_TYPES
from research import (
    RESEARCH_TREE,
    apply_research_effect,
    get_available_research,
    complete_research,
)


class GameState:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.power = 0
        self.oxygen = 100
        self.supplies = 50
        self.max_oxygen = 200
        self.max_supplies = 500
        self.buildings = []
        self.colonists = []
        self.heated_tiles = set()
        self.game_time = 0
        self.event_timer = 180
        self.active_event = None
        self.current_research = None
        self.research_progress = 0
        self.game_over = False
        self.game_over_reason = ""
        self.colonist_efficiency = 1.0
        self.building_degradation_multiplier = 1.0
        self.completed_research = set(["auto_repair", "backup_power"])
        self._setup_starting_colony()

    def _setup_starting_colony(self):
        habitat = Building("habitat", 3, 3)
        self.buildings.append(habitat)
        for _ in range(5):
            self.colonists.append(Colonist(habitat))
        self.buildings.append(Building("power_generator", 1, 1))
        self.buildings.append(Building("power_generator", 6, 1))
        self.buildings.append(Building("life_support", 1, 4))
        self.buildings.append(Building("heater", 3, 2))

    def tick(self):
        if self.game_over:
            return
        self.game_time += 1
        self._calculate_power()
        self._calculate_heat()
        self._degrade_buildings()
        self._produce_resources()
        self._consume_resources()
        self._process_research()
        self._update_events()
        self._check_game_over()

    def _calculate_power(self):
        power_produced = 0
        power_needed = 0
        for building in self.buildings:
            if building.health > 0:
                power_produced += building.power_production
                power_needed += building.power_consumption
        self.power = power_produced
        if power_produced >= power_needed:
            for building in self.buildings:
                building.is_powered = True
        else:
            for building in self.buildings:
                if building.power_consumption == 0:
                    building.is_powered = True
                else:
                    building.is_powered = False

    def _calculate_heat(self):
        self.heated_tiles.clear()
        for building in self.buildings:
            if building.type == "heater" and building.is_functional():
                radius = building.heat_radius
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if abs(dx) + abs(dy) <= radius:
                            tile_x = building.x + dx
                            tile_y = building.y + dy
                            if (
                                0 <= tile_x < self.grid_size
                                and 0 <= tile_y < self.grid_size
                            ):
                                self.heated_tiles.add((tile_x, tile_y))
        for building in self.buildings:
            building.is_heated = any(
                (tx, ty) in self.heated_tiles
                for tx in range(building.x, building.x + building.width)
                for ty in range(building.y, building.y + building.height)
            )

    def _degrade_buildings(self):
        damage = 0.5 * self.building_degradation_multiplier
        if self.active_event and self.active_event.type == "dust_storm":
            damage = 1.0 * self.building_degradation_multiplier
        for building in self.buildings:
            if building.health > 0:
                building.take_damage(damage)

    def _produce_resources(self):
        for building in self.buildings:
            if building.is_functional():
                efficiency = building.get_efficiency()
                if building.output_type == "oxygen":
                    amount = int(building.output_amount * efficiency)
                    self.oxygen = min(self.max_oxygen, self.oxygen + amount)
                elif building.output_type == "supplies":
                    amount = int(building.output_amount * efficiency)
                    self.supplies = min(self.max_supplies, self.supplies + amount)
                elif building.output_type == "repair":
                    if self.game_time % 10 == 0:
                        self._repair_nearby_buildings(building, building.output_amount)

    def _consume_resources(self):
        oxygen_per_colonist = 0.5 * self.colonist_efficiency
        supplies_per_colonist = 0.3 * self.colonist_efficiency
        living_colonists = [c for c in self.colonists if c.is_alive()]
        oxygen_needed = len(living_colonists) * oxygen_per_colonist
        self.oxygen -= oxygen_needed
        supplies_needed = len(living_colonists) * supplies_per_colonist
        self.supplies -= supplies_needed
        if self.oxygen < 0:
            for colonist in living_colonists:
                colonist.take_damage(10)
        if self.supplies < 0:
            for colonist in living_colonists:
                colonist.take_damage(5)

    def _process_research(self):
        if self.current_research:
            self.research_progress += 1
            research_data = RESEARCH_TREE.get(self.current_research)
            if research_data and self.research_progress >= research_data.duration:
                complete_research(self.current_research, self)
                self.current_research = None
                self.research_progress = 0

    def _update_events(self):
        if self.active_event:
            self.active_event.update()
            if self.active_event.is_finished():
                self.active_event = None
        if not self.active_event:
            self.event_timer -= 1
            if self.event_timer <= 0:
                self._trigger_random_event()
                self.event_timer = random.randint(180, 240)

    def _trigger_random_event(self):
        event_types = ["dust_storm", "oxygen_leak", "breakdown"]
        event_type = random.choice(event_types)
        self.active_event = Event(event_type, self)

    def _check_game_over(self):
        living_colonists = [c for c in self.colonists if c.is_alive()]
        if len(living_colonists) == 0:
            self.game_over = True
            self.game_over_reason = "All colonists died"
            return
        life_support_buildings = [
            b for b in self.buildings if b.type == "life_support" and b.health > 0
        ]
        if len(life_support_buildings) == 0:
            self.game_over = True
            self.game_over_reason = "All life support destroyed"
            return

    def can_place_building(self, building_type, x, y):
        if building_type not in BUILDING_TYPES:
            return False

        required_research = BUILDING_TYPES[building_type].get("requires_research")
        if required_research and required_research not in self.completed_research:
            return False

        width = BUILDING_TYPES[building_type]["width"]
        height = BUILDING_TYPES[building_type]["height"]
        if x < 0 or y < 0 or x + width > self.grid_size or y + height > self.grid_size:
            return False
        for building in self.buildings:
            for bx in range(x, x + width):
                for by in range(y, y + height):
                    if building.occupies_tile(bx, by):
                        return False
        return True

    def place_building(self, building_type, x, y):
        if building_type not in BUILDING_TYPES:
            return False

        required_research = BUILDING_TYPES[building_type].get("requires_research")
        if required_research and required_research not in self.completed_research:
            return False

        cost = BUILDING_TYPES[building_type]["cost"]
        if self.supplies >= cost and self.can_place_building(building_type, x, y):
            self.supplies -= cost
            building = Building(building_type, x, y)
            self.buildings.append(building)
            return True
        return False

    def repair_building(self, building):
        repair_cost = 10
        repair_amount = 50
        if self.supplies >= repair_cost and building.health < 100:
            self.supplies -= repair_cost
            building.repair(repair_amount)
            return True
        return False

    def _repair_nearby_buildings(self, repair_drone, amount):
        for building in self.buildings:
            if building == repair_drone:
                continue
            distance = abs(building.x - repair_drone.x) + abs(
                building.y - repair_drone.y
            )
            if distance <= 3 and building.health < 100:
                building.repair(amount)
                break

    def start_research(self, research_id):
        print(f"=== START RESEARCH ===")
        print(f"Research ID: {research_id}")
        print(f"Supplies before: {self.supplies}")

        research = RESEARCH_TREE.get(research_id)

        if not research:
            print(f"Research {research_id} not found")
            return False

        if research_id in self.completed_research:
            print(f"Research already completed")
            return False

        if not research.can_research(self.completed_research):
            print(f"Prerequisites not met")
            return False

        if self.supplies < research.cost:
            print(f"Not enough supplies! Need {research.cost}, have {self.supplies}")
            return False

        self.supplies -= research.cost
        self.current_research = research_id
        self.research_progress = 0

        print(f"Supplies after: {self.supplies}")
        print(f"Current research: {self.current_research}")
        print(f" RESEARCH STARTED ")
        return True

    def _repair_nearby_buildings(self, repair_drone, amount):
        for building in self.buildings:
            if building == repair_drone:
                continue
            distance = abs(building.x - repair_drone.x) + abs(
                building.y - repair_drone.y
            )
            if distance <= 3 and building.health < 100:
                building.repair(amount)
                print(
                    f" Ремонт: {building.type} на ({building.x},{building.y}) восстановлен на {amount}. Здоровье: {building.health}"
                )
                break
