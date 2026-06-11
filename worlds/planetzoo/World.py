from collections.abc import Mapping
from typing import Any

from .Names import LocationNames
from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from . import Options as planetzoo_options
from . import Items, Locations, Regions, Rules


class PlanetZooWorld(World):
    """Planet Zoo Randomizer with Archipelago addition"""
    game = "Planet Zoo"  # name of the game/world
    options_dataclass = planetzoo_options.PlanetZooOptions  # options the player can set
    options: planetzoo_options.PlanetZooOptions  # typing hints for option results
    #settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler
    
    location_name_to_id = Locations.location_name_to_id
    item_name_to_id = Items.item_name_to_id
    startingspecies = [
        "plains_zebra",
        "grey_wolf",
        "american_bison",
        "african_elephant"
    ]
    
    startingmoney = []
    
    
    def create_regions(self) -> None:
        Regions.create_and_connect_regions(self)
        Locations.create_all_locations(self)
    
    def set_rules(self) -> None:
        Rules.set_all_rules(self)
    
    def create_items(self) -> None:
        Items.create_all_items(self)
    
    def create_item(self, name: str) -> Items.PlanetZooItem:
        return Items.create_item_with_correct_classification(self, name)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "starting_money"
        )
    
    def get_filler_item_name(self):
        return Items.get_random_filler_item_name(self)
    
    def create_event(self, event: str) -> Items.PlanetZooItem:
    # while we are at it, we can also add a helper to create events
        return Items.PlanetZooItem(event, ItemClassification.progression, None, self.player)