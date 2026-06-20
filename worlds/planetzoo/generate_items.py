from enum import Enum
import json
import re
from pydantic import BaseModel
from typing import Dict, List

# How it currently looks


class AnimalEntry(BaseModel):
    level: str
    next: List[str]
    rewards: List[str]


class MechanicOption(BaseModel):
    item: str
    entry_level: bool
    enabled: bool
    completed: bool
    next: List[str]


class StartUnlockedOption(BaseModel):
    entity: str
    level: str


class GameData(BaseModel):
    species: Dict[str, List[AnimalEntry]]
    mechanic: Dict[str, List[MechanicOption]]
    start_unlocked: Dict[str, List[StartUnlockedOption]]


class APClass(str, Enum):
    filler = "Filler"
    progression = "Progression"
    useful = "Useful"
    trap = "Trap"
    normal = "Normal"


class Version(str, Enum):
    base = "Base"

# Adding in species permit using species.json


class Interactivity(str, Enum):
    full = "full"
    exhibit = "exhibit"


class SpeciesesFormation(BaseModel):
    stringid: str
    label: str
    interactivity: Interactivity
    water_needed: bool
    fence_grade: int

    # {
    #     "stringid": "aardvark",
    #     "label": "Aardvark",
    #     "interactivity": "full"
    # },


# How I want it to look
class ItemsData(BaseModel):
    name: str
    ap_classification: APClass
    version: Version
    quantity: int

# Call for creating permits for each species


def species_to_permit_item(species: SpeciesesFormation) -> list[ItemsData]:
    unique_items: list[ItemsData] = []
    # Add permit per species
    unique_items.append(ItemsData(
        name=f"Permit: {species.label}",
        ap_classification="Progression",
        version=Version.base,
        quantity=1
    ))
    return unique_items


with open("ArchipelagoPZ\worlds\planetzoo\data\specieses.json") as json_file:
    json_data = json.load(json_file)
    lfl = [SpeciesesFormation.model_validate(
        loopstuff)for loopstuff in json_data]
    # location formation list
unique_items: list[ItemsData] = []
for species in lfl:
    unique_items.extend(species_to_permit_item(species))


def convert_readable(name: str) -> str:
    name = re.sub(r'^EN_', 'Enrichment: ', name)        # Remove EN_ prefix
    name = name.replace('_', ' ')           # Replace underscores with spaces
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)  # Split camelCase
    # Split letters from numbers
    name = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', name)
    name = name.replace(' L ', ' Level ')
    return name.strip()


def get_classification(name: str, section: str = None) -> APClass:
    if name.startswith("EN_"):
        return APClass.useful
    if section in [
            "default_off_stafffacilities", "default_on_stafffacilities", "default_off_power", "default_on_power"]:
        return APClass.useful
    if section in ["default_off_barriers", "default_on_barriers"]:
        return APClass.progression
    return APClass.normal


with open("ArchipelagoPZ\worlds\planetzoo\data\\research_catalog.json") as json_file:
    json_data = json.load(json_file)
    # research_cat_list = [GameData.model_validate(loopstuff) for loopstuff in json_data]

data = GameData(**json_data)
unique_items = {item.name: item for item in unique_items}


for species, animal_list in data.species.items():
    # unique_items[species] = ItemsData(
    #     name=f"Permit: {species}",
    #     ap_classification="Progression",
    #     version=Version.base,
    #     quantity=1
    # )
    for this_animal in animal_list:
        for reward in this_animal.rewards:
            if any(word in reward for word in ["Zoopedia", "Breeding", "Education", "Supplement", "EnrichmentL", "DLC"]):
                continue
            else:
                unique_items[reward] = ItemsData(
                    name=convert_readable(reward),
                    ap_classification=get_classification(reward),
                    version=Version.base,
                    quantity=1
                )


for section_name, option_list in data.mechanic.items():
    for this_option in option_list:
        if this_option.item not in unique_items:
            if any(word in this_option.item for word in ["Barriers"]):
                continue
            else:
                unique_items[this_option.item] = ItemsData(
                    name=convert_readable(this_option.item),
                    ap_classification=get_classification(
                        this_option.item, section_name),
                    version=Version.base,
                    quantity=1
                )

# Add other items to the list: Old items from olditems.json, and permits for every animal? Animal groups?

sorted_items = sorted(unique_items.values(), key=lambda x: x.name)
output = [item.model_dump() for item in sorted_items]

with open("ArchipelagoPZ\worlds\planetzoo\data\\items.json", "w") as output_file:
    json.dump(output, output_file)
