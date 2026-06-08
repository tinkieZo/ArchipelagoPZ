from dataclasses import dataclass
from Options import PerGameCommonOptions, Range


class StartingMoney(Range):
    """Amount of money to start with"""
    display_name = "Starting Money"
    range_start = 10000
    range_end = 2000000
    default = 50000


# class starting_species(Range):
#     """Number of species unlocked at start"""
#     display_name = "Species Unlocked"
#     range_start = 1
#     range_end = 10 #Total number of available species
#     default = 3


# @dataclass
# class PlanetZooOptions(PerGameCommonOptions):
#     num_starting_species:starting_species

@dataclass
class PlanetZooOptions(PerGameCommonOptions):
    starting_money: StartingMoney

