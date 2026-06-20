from dataclasses import dataclass
from Options import PerGameCommonOptions, Range


class StartingMoney(Range):
    """Amount of money to start with"""
    display_name = "Starting Money"
    range_start = 10000
    range_end = 2000000
    default = 50000


class StartingSpecies(Range):
    """Number of species unlocked at start"""
    display_name = "Species Unlocked"
    range_start = 1
    range_end = 78  # Total number of available species
    default = 3


class StartingBarrierLevel(Range):
    """What barrier level should be start with"""
    display_name = "Barriers Unlocked"
    range_start = 0
    range_end = 6
    default = 1


@dataclass
class PlanetZooOptions(PerGameCommonOptions):
    starting_money: StartingMoney
    num_starting_species: StartingSpecies
    barrier_lvl_start: StartingBarrierLevel
