from __future__ import annotations
import json
import pkgutil
from typing import TYPE_CHECKING, List
import typing
from BaseClasses import ItemClassification, Location
from .Names import ItemNames, LocationNames, RegionNames
from collections import namedtuple
from .Items import PlanetZooItem

if TYPE_CHECKING:
    from .World import PlanetZooWorld



def location_decoder(objdict):
    return namedtuple('DefaultLocation', objdict.keys())(*objdict.values())

class LocationData(typing.NamedTuple):
    LocationName: str


complete_location_list:List[LocationData] = []
default_location_list = {}

default_location_list = json.loads(pkgutil.get_data(__name__, "data/location.json"), object_hook=location_decoder)
for location in default_location_list:
    complete_location_list.append(LocationData(location.name))



location_name_to_id = {
    loc_name.LocationName: 2000 + index for index, loc_name in enumerate(complete_location_list)
}

class PlanetZooLocation(Location):
    game = "Planet Zoo"



research_locations_names = [
    LocationNames.rw_plains_zebra, 
    LocationNames.rw_grey_wolf, 
    LocationNames.rw_american_bison,
    LocationNames.rw_bengal_tiger, 
    LocationNames.rw_african_elephant, 
    LocationNames.rw_nile_hippo, 
    LocationNames.rw_saltwater_croc, 
    LocationNames.rw_snow_leopard, 
    LocationNames.rw_w_l_gorilla, 
    LocationNames.rw_giant_panda,   
]

mechanic_locations_names = [
    LocationNames.rmech_drink_shops,
    LocationNames.rmech_advanced_barriers
]

breeding_locations_names = [
    LocationNames.fb_plains_zebra, 
    LocationNames.fb_grey_wolf, 
    LocationNames.fb_bengal_tiger,
    LocationNames.fb_w_l_gorilla, 
    LocationNames.fb_giant_panda
]

milestones_locations_names = [
    LocationNames.ms_zoo_2_stars, 
    LocationNames.ms_1000_guests, 
    LocationNames.ms_first_conserv_release,
    #LocationNames.ms_flagship_reached
]

conservation_locations_names = []
all_locations = [
    research_locations_names, 
    mechanic_locations_names,
    breeding_locations_names,
    milestones_locations_names,
    conservation_locations_names]

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: location_name_to_id[location_name] for location_name in location_names}

def create_all_locations(world: PlanetZooWorld) -> None:
    create_regular_locations(world)
    create_goal_location(world)


def create_regular_locations(world: PlanetZooWorld) -> None:
    research_locations = world.multiworld.get_region(RegionNames.research_tree, world.player)
    mechanic_locations = world.multiworld.get_region(RegionNames.mechanic_tree , world.player)
    conservation_locations = world.multiworld.get_region(RegionNames.conservation_credits, world.player)
    milestones_locations = world.multiworld.get_region(RegionNames.milestones, world.player)
    breeding_locations = world.multiworld.get_region(RegionNames.breeding, world.player)

    set_research_locations = get_location_names_with_ids(
        research_locations_names)
    research_locations.add_locations(set_research_locations, PlanetZooLocation)

    set_mechanic_locations = get_location_names_with_ids(
        mechanic_locations_names)
    mechanic_locations.add_locations(set_mechanic_locations, PlanetZooLocation)

    set_conservation_locations = get_location_names_with_ids(
        conservation_locations_names)
    conservation_locations.add_locations(set_conservation_locations, PlanetZooLocation)

    set_milestones_locations = get_location_names_with_ids(
        milestones_locations_names)
    milestones_locations.add_locations(set_milestones_locations, PlanetZooLocation)

    #Remove fb_giant_panda out of the normal location pool

    filtered_breeding_locations = [loc for loc in breeding_locations_names if loc != LocationNames.fb_giant_panda]
    set_breeding_locations = get_location_names_with_ids(
        filtered_breeding_locations)
    breeding_locations.add_locations(set_breeding_locations, PlanetZooLocation)


#Current goal option : Breed Pandas
def create_goal_location(world: PlanetZooWorld) -> None:
    region = world.multiworld.get_region(RegionNames.menu, world.player)
    goal_location = PlanetZooLocation(world.player, LocationNames.fb_giant_panda, None, region)
    region.locations.append(goal_location)
