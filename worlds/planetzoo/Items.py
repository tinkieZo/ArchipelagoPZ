from __future__ import annotations
from collections import namedtuple
from enum import Enum
import json
import pkgutil
from random import sample
from typing import TYPE_CHECKING, List
import typing
from dataclasses import dataclass

from pydantic import BaseModel


from BaseClasses import Item, ItemClassification
from .Names import ItemNames

if TYPE_CHECKING:
    from .World import PlanetZooWorld

# Creater list of Items


@dataclass
class ItemData:
    name: str
    progression: ItemClassification
    quantity: int


def convert_ap_class(ap_string):
    # Create list of Items
    ap_class = ItemClassification.useful
    # print(item)
    match ap_string:
        case "Filler":
            ap_class = ItemClassification.filler
        case "Progression":
            ap_class = ItemClassification.progression
        case "Useful":
            ap_class = ItemClassification.useful
        case "Trap":
            ap_class = ItemClassification.trap
        case "SkipBalancing":
            ap_class = ItemClassification.skip_balancing
        case "ProgressionSkipBalancing":
            ap_class = ItemClassification.progression_skip_balancing
    return ap_class


def item_decoder(objdict):
    return namedtuple('DefaultItem', objdict.keys())(*objdict.values())


def get_item_by_name(name: str) -> ItemData | None:
    return next(
        (item for item in complete_item_list if item.name == name),
        None
    )


# Special items added with olditems.json
complete_item_list: List[ItemData] = []
default_item_list = {}
old_item_list = {}
basic_items_list = json.loads(pkgutil.get_data(
    __name__, "data/items.json"), object_hook=item_decoder)
special_items_list = json.loads(pkgutil.get_data(
    __name__, "data/old_items.json"), object_hook=item_decoder)

default_item_list = basic_items_list + special_items_list

for item in default_item_list:
    complete_item_list.append(
        ItemData(item.name, convert_ap_class(item.ap_classification), item.quantity))
item_name_to_id = {data.name: 1000 + index for index,
                   data in enumerate(complete_item_list)}
# Don't reload old files :D
# Fix later: Can't run old world if ID's are redone
# Pech

# Access species fence gate


class Interactivity(str, Enum):
    full = "full"
    exhibit = "exhibit"


class SpeciesesFormation(BaseModel):
    stringid: str
    label: str
    interactivity: Interactivity
    water_needed: bool
    fence_grade: int


species_data = json.loads(pkgutil.get_data(
    __name__, "data/specieses.json"))

species_data_list = [SpeciesesFormation.model_validate(
    loopstuff)for loopstuff in species_data]


class PlanetZooItem(Item):
    game = "Planet Zoo"


def create_item_with_correct_classification(world: PlanetZooWorld, name: str) -> PlanetZooItem:
    item = get_item_by_name(name)
    if (item):
        classification = item.progression
    else:
        classification = ItemClassification.filler  # avoid unassigned variable crashes
    return PlanetZooItem(name, classification, item_name_to_id[name], world.player)


def get_random_filler_item_name(world: PlanetZooWorld) -> str:
    roll = world.random.randint(0, 99)
    if roll < 5:
        return ItemNames.cash_inject_l
    if roll < 25:
        return ItemNames.cash_inject_m
    if roll < 50:
        return ItemNames.cash_inject_s
    if roll < 55:
        return ItemNames.conserv_cred_l
    if roll < 75:
        return ItemNames.conserv_cred_m
    return ItemNames.conserv_cred_s


# Permit list for Rule
list_of_permits = [
    item.name for item in complete_item_list if
    "Permit" in item.name
]


def create_all_items(world: PlanetZooWorld) -> None:
    list_of_permits = [
        item for item in complete_item_list if
        "Permit" in item.name and "Giant Panda" not in item.name
    ]
    list_of_lv0_animals = [
        item for item in species_data_list if item.fence_grade == 0
    ]
    list_of_lv1_animals = [
        item for item in species_data_list if item.fence_grade == 1
    ]
    lvl0_animal_names = {animal.label for animal in list_of_lv0_animals}
    lvl1_animal_names = {animal.label for animal in list_of_lv1_animals}
    permits_for_lv0_animals = [
        permit for permit in list_of_permits
        if permit.name.split(": ")[1] in lvl0_animal_names
    ]
    permits_for_lv1_animals = [
        permit for permit in list_of_permits
        if permit.name.split(": ")[1] in lvl1_animal_names
    ]

    if world.options.barrier_lvl_start == 0:
        check_settings = permits_for_lv0_animals
    elif world.options.barrier_lvl_start == 1:
        check_settings = permits_for_lv1_animals
    else:
        check_settings = list_of_permits

    starting_animals = sample(
        check_settings, world.options.num_starting_species)
    # starting_animals = sample(
    #     list_of_permits, world.options.num_starting_species)
    starting_animals_names = {item.name for item in starting_animals}
    reduced_item_list = [
        item for item in complete_item_list if item.name not in starting_animals_names]
    if world.options.barrier_lvl_start > 0:
        progressive_barrier = next(
            item for item in reduced_item_list if item.name == "Progressive Barrier Level")
        progressive_barrier.quantity -= world.options.barrier_lvl_start
        for _ in range(world.options.barrier_lvl_start):
            starting_animals.append(
                ItemData("Progressive Barrier Level", ItemClassification.progression, 1))

    for item in starting_animals:
        world.multiworld.push_precollected(
            create_item_with_correct_classification(world, item.name))
    for item in reduced_item_list:
        world.multiworld.itempool.append(
            create_item_with_correct_classification(world, item.name))
        if item.quantity > 1:
            for _ in range(item.quantity-1):
                world.multiworld.itempool.append(
                    create_item_with_correct_classification(world, item.name))

    number_of_items = len(world.multiworld.itempool)
    number_of_unfilled_locations = len(
        world.multiworld.get_unfilled_locations(world.player))
    # print(world.multiworld.get_unfilled_locations(world.player))  # Test
    needed_number_of_filler_items = number_of_unfilled_locations - \
        number_of_items-1  # Takes the goal location out of the location choices
    # Can filter out the goal location, instead of doing -1 (fix for later)
    world.multiworld.itempool += [world.create_filler()
                                  for _ in range(needed_number_of_filler_items)]
