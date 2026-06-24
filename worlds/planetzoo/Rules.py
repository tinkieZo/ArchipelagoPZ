from __future__ import annotations
from functools import reduce
from typing import TYPE_CHECKING
from rule_builder.rules import Has, HasAllCounts, HasGroup
from .Items import ItemNames, list_of_permits
from .Names import EntranceNames
from .Locations import LocationFormation, complete_location_list
if TYPE_CHECKING:
    from .World import PlanetZooWorld


HAS_CENTRE = Has(ItemNames.research_centre)
HAS_WORKSHOP = Has(ItemNames.workshop)
HAS_CONS_PROG = Has(ItemNames.conserve_program)
HAS_WATER_TOOLS = Has(ItemNames.water_hab_tools)
guest_counts_to_species = {"250": 0,
                           "500": 4,
                           "750": 6,
                           "1000": 8,
                           "1250": 10,
                           "2500": 18}


def set_all_rules(world: PlanetZooWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

# Research and Mechanics require buildings to be accessible


def set_all_entrance_rules(world: PlanetZooWorld) -> None:
    menu_to_research = world.multiworld.get_entrance(
        EntranceNames.menu_to_research, world.player)
    world.set_rule(menu_to_research, HAS_CENTRE)

    menu_to_mechanic = world.multiworld.get_entrance(
        EntranceNames.menu_to_mechanic, world.player)
    world.set_rule(menu_to_mechanic, HAS_WORKSHOP)
 # Need to release at least one animal to unlock Conservation Program
    cons_program = world.multiworld.get_entrance(
        EntranceNames.menu_to_conservation, world.player)
    world.set_rule(cons_program, HAS_CONS_PROG)


# Logic graph integrated here?
def set_all_location_rules(world: PlanetZooWorld) -> None:
    # Animals that area gated rules are here
    # Permits for seperate animals

    for location in complete_location_list:
        condition = []
        if location.label == "First Breeding - Giant Panda":
            continue
        if location.species_type != "none":
            animal_name = location.label.split(" - ")[1]
            animal_permit = f"Permit: {animal_name}"
            condition.append(Has(animal_permit))
            if location.water_needed == True:
                condition.append(HAS_WATER_TOOLS)
                # Water check rule
            if location.fence_grade > 0:
                condition.append(Has(
                    "Progressive Barrier Level", location.fence_grade))
        if "guests" in location.stringid:
            guest_count = location.label.split(" - ")[1]
            condition.append(
                HasGroup('Permits', guest_counts_to_species[guest_count])
            )
        if condition:
            current_location = world.multiworld.get_location(
                location.label, world.player)
            combined_rule = reduce(lambda a, b: a & b, condition)
            world.set_rule(current_location, combined_rule)


# Goal currently is, breed Giant Pandas
def set_completion_condition(world: PlanetZooWorld) -> None:
    goal_location = world.multiworld.get_location("First Breeding - Giant Panda",
                                                  world.player)
    goal_location.place_locked_item(world.create_event("Victory"))
    world.set_rule(goal_location, HasAllCounts(
        {"Permit: Giant Panda": 1, "Progressive Barrier Level": 4}))
    world.multiworld.completion_condition[world.player] = lambda state: state.has(
        "Victory", world.player)
