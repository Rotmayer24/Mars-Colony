class Research:
    def __init__(
        self, research_id, name, description, cost, duration, tier, prerequisites
    ):
        self.id = research_id
        self.name = name
        self.description = description
        self.cost = cost
        self.duration = duration
        self.tier = tier
        self.prerequisites = prerequisites
        self.effect = None

    def can_research(self, completed_research):
        for prereq in self.prerequisites:
            if prereq not in completed_research:
                return False
        return True


RESEARCH_TREE = {
    "efficient_panels": Research(
        "efficient_panels",
        "Efficient Panels",
        "Solar panels produce +2 energy",
        60,
        60,
        1,
        [],
    ),
    "improved_insulation": Research(
        "improved_insulation",
        "Improved Insulation",
        "Heaters heat 6 tiles instead of 4",
        50,
        50,
        1,
        [],
    ),
    "advanced_life_support": Research(
        "advanced_life_support",
        "Advanced Life Support",
        "Life support produces +1 oxygen",
        80,
        80,
        2,
        ["efficient_panels"],
    ),
    "auto_repair": Research(
        "auto_repair",
        "Automatic Repair",
        "Unlocks Repair Drone building",
        100,
        100,
        2,
        ["improved_insulation"],
    ),
    "hydroponics": Research(
        "hydroponics",
        "Hydroponics",
        "Greenhouses produce +1 supplies",
        120,
        120,
        3,
        ["advanced_life_support", "auto_repair"],
    ),
    "backup_power": Research(
        "backup_power",
        "Backup Power",
        "Unlocks Battery building",
        150,
        150,
        3,
        ["advanced_life_support", "auto_repair"],
    ),
    "colony_optimization": Research(
        "colony_optimization",
        "Colony Optimization",
        "Colonists consume 30% less resources",
        200,
        200,
        4,
        ["hydroponics", "backup_power"],
    ),
    "reinforced_modules": Research(
        "reinforced_modules",
        "Reinforced Modules",
        "Buildings degrade 50% slower",
        180,
        180,
        4,
        ["hydroponics", "backup_power"],
    ),
}


def apply_research_effect(research_id, game_state):
    from building import BUILDING_TYPES

    if research_id == "efficient_panels":
        BUILDING_TYPES["power_generator"]["power_production"] = 12

    elif research_id == "improved_insulation":
        BUILDING_TYPES["heater"]["heat_radius"] = 6
        if hasattr(game_state, "buildings"):
            for building in game_state.buildings:
                if building.type == "heater":
                    building.heat_radius = 6

    elif research_id == "advanced_life_support":
        BUILDING_TYPES["life_support"]["output_amount"] = 6

    elif research_id == "auto_repair":
        pass

    elif research_id == "hydroponics":
        BUILDING_TYPES["greenhouse"]["output_amount"] = 4

    elif research_id == "backup_power":
        pass

    elif research_id == "colony_optimization":
        if hasattr(game_state, "colonist_efficiency"):
            game_state.colonist_efficiency = 0.7

    elif research_id == "reinforced_modules":
        if hasattr(game_state, "building_degradation_multiplier"):
            game_state.building_degradation_multiplier = 0.5


def get_available_research(completed_research):
    available = []
    for research_id, research in RESEARCH_TREE.items():
        if research_id not in completed_research:
            if research.can_research(completed_research):
                available.append(research)
    return available


def get_research_by_id(research_id):
    return RESEARCH_TREE.get(research_id)


def start_research(research_id, game_state):
    research = get_research_by_id(research_id)

    if not research:
        return False

    if research_id in game_state.completed_research:
        return False

    if not research.can_research(game_state.completed_research):
        return False

    if game_state.supplies < research.cost:
        return False

    game_state.supplies -= research.cost
    game_state.current_research = research_id
    game_state.research_progress = 0
    return True


def complete_research(research_id, game_state):
    research = get_research_by_id(research_id)

    if not research:
        return False

    apply_research_effect(research_id, game_state)
    game_state.completed_research.add(research_id)
    return True
