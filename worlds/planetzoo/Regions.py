from __future__ import annotations

from typing import TYPE_CHECKING

import typing

from .Names import RegionNames, EntranceNames
from .Locations import research_locations_names, mechanic_locations_names, conservation_locations_names, milestones_locations_names, breeding_locations_names
from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .World import PlanetZooWorld

class RegionInfo(typing.NamedTuple):
    name: str
    locations: typing.List[str]


all_regions = [
    RegionInfo(RegionNames.menu, []),
    RegionInfo(RegionNames.research_tree, research_locations_names),
    RegionInfo(RegionNames.mechanic_tree, mechanic_locations_names),
    RegionInfo(RegionNames.conservation_credits, conservation_locations_names),
    RegionInfo(RegionNames.milestones, milestones_locations_names),
    RegionInfo(RegionNames.breeding, breeding_locations_names)
]   
regions_by_name: typing.Dict[str, RegionInfo] = {region.name: region for region in all_regions}

def create_and_connect_regions(world: PlanetZooWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: PlanetZooWorld) -> None:
    menu = Region(RegionNames.menu, world.player, world.multiworld)
    research_locations = Region(RegionNames.research_tree, world.player, world.multiworld)
    mechanic_locations = Region(RegionNames.mechanic_tree, world.player, world.multiworld)
    conservation_locations = Region(RegionNames.conservation_credits, world.player, world.multiworld)
    milestones_locations = Region(RegionNames.milestones, world.player, world.multiworld)
    breeding_locations = Region(RegionNames.breeding, world.player, world.multiworld)

    regions = [menu, research_locations, mechanic_locations, conservation_locations, milestones_locations, breeding_locations]

    # Option for if it only exists if player enables certain options
    # if world.options.placeholder_option:
    #     seperate_location = Region("Seperate Location", world.player, world.multiworld)
    #     regions.append(seperate_location)

    world.multiworld.regions += regions

def connect_regions(world: PlanetZooWorld) -> None:
    menu = world.multiworld.get_region(RegionNames.menu, world.player)
    research = world.multiworld.get_region(RegionNames.research_tree, world.player)
    mechanic = world.multiworld.get_region(RegionNames.mechanic_tree, world.player)
    conservation = world.multiworld.get_region(RegionNames.conservation_credits, world.player)
    milestones = world.multiworld.get_region(RegionNames.milestones, world.player)
    breeding = world.multiworld.get_region(RegionNames.breeding, world.player)

    menu_to_research = Entrance(world.player, EntranceNames.menu_to_research, parent = menu)
    menu.exits.append(menu_to_research)
    menu_to_research.connect(research)

    menu_to_mechanic = Entrance(world.player, EntranceNames.menu_to_mechanic, parent = menu)
    menu.exits.append(menu_to_mechanic)
    menu_to_mechanic.connect(mechanic)
    
    menu_to_conservation = Entrance(world.player, EntranceNames.menu_to_conservation, parent = menu)
    menu.exits.append(menu_to_conservation)
    menu_to_conservation.connect(conservation)

    menu_to_milestones = Entrance(world.player, EntranceNames.menu_to_milestones, parent = menu)
    menu.exits.append(menu_to_milestones)
    menu_to_milestones.connect(milestones)

    menu_to_breeding = Entrance(world.player, EntranceNames.menu_to_breeding, parent = menu)
    menu.exits.append(menu_to_breeding)
    menu_to_breeding.connect(breeding)

