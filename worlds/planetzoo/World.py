from collections.abc import Mapping
from typing import Any

from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from . import Options as planetzoo_options
from . import Items, Locations, Regions, Rules


class PlanetZooWorld(World):
    """Planet Zoo Randomizer with Archipelago addition"""
    game = "Planet Zoo"  # name of the game/world
    options_dataclass = planetzoo_options.PlanetZooOptions  # options the player can set
    options: planetzoo_options.PlanetZooOptions  # typing hints for option results
    # settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    location_name_to_id = Locations.location_name_to_id
    item_name_to_id = Items.item_name_to_id

    item_name_groups = {
        "Permits": Items.list_of_permits,
    }

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

    def get_filler_item_name(self):
        return Items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        GOAL = {
            "type": "breed",
            "args": {
                "required_breed": ["gpanda"],  # breed a Giant Panda
                "required_research": [],
            },
        }
        data = self.options.as_dict("starting_money", "num_starting_species")
        data["goal"] = GOAL
        return data

    def create_event(self, event: str) -> Items.PlanetZooItem:
        return Items.PlanetZooItem(event, ItemClassification.progression, None, self.player)
