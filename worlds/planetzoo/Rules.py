from __future__ import annotations
from typing import TYPE_CHECKING
from rule_builder.rules import Has
from .Items import ItemNames
from .Names import EntranceNames
from .Locations import LocationFormation, complete_location_list
if TYPE_CHECKING:
    from .World import PlanetZooWorld


HAS_CENTRE = Has(ItemNames.research_centre)
HAS_WORKSHOP = Has(ItemNames.workshop)
HAS_CONS_PROG = Has(ItemNames.conserve_program)
HAS_WATER_TOOLS = Has(ItemNames.water_hab_tools)


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
        if location.stringid == "fb_gpanda":
            continue
        if location.species_type != "none":
            animal_name = location.label.split(" - ")[1]
            animal_permit = f"Permit: {animal_name}"
            current_location = world.multiworld.get_location(
                location.stringid, world.player)
            world.set_rule(current_location, Has(animal_permit))
            if location.water_needed == True:
                world.set_rule(current_location, HAS_WATER_TOOLS)
                # Water check rule


# Goal currently is, breed Giant Pandas
def set_completion_condition(world: PlanetZooWorld) -> None:
    goal_location = world.multiworld.get_location("fb_gpanda",
                                                  world.player)
    goal_location.place_locked_item(world.create_event("Victory"))
    world.set_rule(goal_location, Has(
        item_name="Permit: Giant Panda"))
    world.multiworld.completion_condition[world.player] = lambda state: state.has(
        "Victory", world.player)
