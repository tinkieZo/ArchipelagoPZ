from __future__ import annotations
from enum import Enum
import json
from typing import TYPE_CHECKING, List
import typing

from pydantic import BaseModel
from BaseClasses import Location
from .Names import RegionNames
from pydantic import BaseModel


if TYPE_CHECKING:
    from .World import PlanetZooWorld


class LocationFormation(BaseModel):
    stringid: str
    label: str
    type: LocationType
    species_type: str
    water_needed: bool


class LocationType(str, Enum):
    research_welfare = "research welfare"
    firsts = "firsts"
    conservation = "conservation"
    mechanic = "mechanic"
    milestones = "milestones"


class LocationData(typing.NamedTuple):
    LocationName: str


with open("ArchipelagoPZ\worlds\planetzoo\data\specieslocations.json", "r") as species_json_file:
    species_location_data = json.load(species_json_file)


species_location_list: List[LocationFormation] = [
    LocationFormation(**item) for item in species_location_data]

with open("ArchipelagoPZ\worlds\planetzoo\data\mech_n_milestones.json", "r") as mech_n_milestones_json_file:
    mech_n_milestones_data = json.load(mech_n_milestones_json_file)


mech_n_milestones_list: List[LocationFormation] = [
    LocationFormation(**item) for item in mech_n_milestones_data]

complete_location_list = species_location_list + mech_n_milestones_list

location_name_to_id = {
    loc_name.stringid: 2000 + index for index, loc_name in enumerate(complete_location_list)
}


class PlanetZooLocation(Location):
    game = "Planet Zoo"


research_locations_names = [
    location
    for location in complete_location_list
    if location.type == LocationType.research_welfare
]
# list(filter(lamba l: l.type == LocationType.research_welfare), complete_location_list)
# Daten umwandelung:
# filter, map, reduce

mechanic_locations_names = [
    location
    for location in complete_location_list
    if location.type == LocationType.mechanic
]

firsts_locations_names = [
    location
    for location in complete_location_list
    if location.type == LocationType.firsts
]

milestones_locations_names = [
    location
    for location in complete_location_list
    if location.type == LocationType.milestones
]

conservation_locations_names = [
    location
    for location in complete_location_list
    if location.type == LocationType.conservation
]

all_locations = [
    research_locations_names,
    mechanic_locations_names,
    firsts_locations_names,
    milestones_locations_names,
    conservation_locations_names]


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name.stringid: location_name_to_id[location_name.stringid] for location_name in location_names}


def create_all_locations(world: PlanetZooWorld) -> None:
    create_regular_locations(world)
    create_goal_location(world)


def create_regular_locations(world: PlanetZooWorld) -> None:
    research_locations = world.multiworld.get_region(
        RegionNames.research, world.player)
    mechanic_locations = world.multiworld.get_region(
        RegionNames.mechanic, world.player)
    conservation_locations = world.multiworld.get_region(
        RegionNames.conservation, world.player)
    milestones_locations = world.multiworld.get_region(
        RegionNames.milestones, world.player)
    firsts_locations = world.multiworld.get_region(
        RegionNames.firsts, world.player)

    set_research_locations = get_location_names_with_ids(
        research_locations_names)
    research_locations.add_locations(set_research_locations, PlanetZooLocation)

    set_mechanic_locations = get_location_names_with_ids(
        mechanic_locations_names)
    mechanic_locations.add_locations(set_mechanic_locations, PlanetZooLocation)

    set_conservation_locations = get_location_names_with_ids(
        conservation_locations_names)
    conservation_locations.add_locations(
        set_conservation_locations, PlanetZooLocation)

    set_milestones_locations = get_location_names_with_ids(
        milestones_locations_names)
    milestones_locations.add_locations(
        set_milestones_locations, PlanetZooLocation)

    # Remove fb_giant_panda out of the normal location pool

    filtered_firsts_locations = [
        loc for loc in firsts_locations_names if loc.stringid != "fb_gpanda"]
    set_firsts_locations = get_location_names_with_ids(
        filtered_firsts_locations)
    firsts_locations.add_locations(set_firsts_locations, PlanetZooLocation)

# Current goal option : Breed Pandas


def create_goal_location(world: PlanetZooWorld) -> None:
    region = world.multiworld.get_region(RegionNames.menu, world.player)
    panda_location = next(
        loc for loc in complete_location_list if loc.stringid == "fb_gpanda")
    goal_location = PlanetZooLocation(
        world.player, panda_location.stringid, None, region)
    region.locations.append(goal_location)
