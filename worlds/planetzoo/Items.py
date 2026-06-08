from __future__ import annotations
from collections import namedtuple
import json
import pkgutil
from typing import TYPE_CHECKING, List
import typing


from BaseClasses import Item, ItemClassification
from .Names import ItemNames

if TYPE_CHECKING:
    from .World import PlanetZooWorld

#Creater list of Items
class ItemData(typing.NamedTuple):
    itemName: str
    progression: ItemClassification

def convert_ap_class(ap_string):
    # Create list of Items
    ap_class = ItemClassification.useful
    #print(item)
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
        (item for item in complete_item_list if item.itemName == name),
        None
    )

complete_item_list:List[ItemData] = []
default_item_list = {}
default_item_list = json.loads(pkgutil.get_data(__name__, "data/items.json"), object_hook=item_decoder)
for item in default_item_list:
    complete_item_list.append(ItemData(item.name, convert_ap_class(item.ap_classification)))
item_name_to_id = {data.itemName: 1000 + index for index, data in enumerate(complete_item_list)}


class PlanetZooItem(Item):
    game = "Planet Zoo"

def create_item_with_correct_classification(world: PlanetZooWorld, name: str) -> PlanetZooItem:
    item=get_item_by_name(name)
    if(item):
        classification=item.progression
    return PlanetZooItem(name, classification, item_name_to_id[name], world.player)

def get_random_filler_item_name(world: PlanetZooWorld) -> str:
    roll = world.random.randint(0,99)
    if roll<16:
        return ItemNames.cash_inject_l
    if roll<33:
        return ItemNames.cash_inject_m
    if roll<50:
        return ItemNames.cash_inject_s
    if roll<66:
        return ItemNames.conserv_cred_l
    if roll<84:
        return ItemNames.conserv_cred_m
    return ItemNames.conserv_cred_s

def create_all_items(world: PlanetZooWorld) -> None:
    # itempool: list[Item] = [
    #     world.create_item(ItemNames.research_centre),
    #     world.create_item(ItemNames.workshop),
    #     world.create_item(ItemNames.water_hab_tools),
    #     world.create_item(ItemNames.conserve_program),
    #     world.create_item(ItemNames.permit_saltwater_croc),
    #     world.create_item(ItemNames.permit_w_l_gorilla),
    #     world.create_item(ItemNames.permit_bengal_tiger),
    #     world.create_item(ItemNames.permit_snow_leopard),
    #     world.create_item(ItemNames.permit_giant_panda),
    #     world.create_item(ItemNames.cash_inject_m),
    #     world.create_item(ItemNames.cash_inject_l),
    #     world.create_item(ItemNames.conserv_cred_l),
    #     world.create_item(ItemNames.cash_inject_s),
    #     world.create_item(ItemNames.conserv_cred_s),
    #     world.create_item(ItemNames.conserv_cred_m),
    # ]

    for item in complete_item_list:
        world.multiworld.itempool.append(create_item_with_correct_classification(world,item.itemName))

    number_of_items = len(world.multiworld.itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    world.multiworld.itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]






#items_by_name: typing.Dict[str, ItemData] = {item.itemName: item for item in all_items}