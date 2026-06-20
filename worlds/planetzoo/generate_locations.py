import json
from pydantic import BaseModel
from enum import Enum


class LocationType(str, Enum):
    research_welfare = "research welfare"
    firsts = "firsts"
    conservation = "conservation"
    mechanic = "mechanic"


class Interactivity(str, Enum):
    full = "full"
    exhibit = "exhibit"


# Create a template here?
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


class LocationFormation(BaseModel):
    stringid: str
    label: str
    type: LocationType
    species_type: str
    water_needed: bool
    fence_grade: int

    # {
    #     "stringid" : "welfare1_aardvark",
    #     "label" : "Research Welfare 1 - Aardvark",
    #     "type" : "Research Welfare"
    #       "species_type" : "aardvark" / None (mechanical/milestones)
    # },


def species_to_locations(species: SpeciesesFormation) -> list[LocationFormation]:
    locations: list[LocationFormation] = []
    # Add species specific checks
    if species.interactivity == Interactivity.full:
        for i in range(6):
            locations.append(LocationFormation(
                stringid=f"welfare{i+1}_{species.stringid}",
                label=f"Research Welfare {i+1} - {species.label}",
                type=LocationType.research_welfare,
                species_type=species.stringid,
                water_needed=species.water_needed,
                fence_grade=species.fence_grade
            ))
    else:
        for i in range(3):
            locations.append(LocationFormation(
                stringid=f"e_welfare{i+1}_{species.stringid}",
                label=f"Research Welfare {i+1} - {species.label}",
                type=LocationType.research_welfare,
                species_type=species.stringid,
                water_needed=False,
                fence_grade=species.fence_grade
            ))

    locations.append(LocationFormation(
        stringid=f"fb_{species.stringid}",
        label=f"First Breeding - {species.label}",
        type=LocationType.firsts,
        species_type=species.stringid,
        water_needed=species.water_needed,
        fence_grade=species.fence_grade
    ))
    locations.append(LocationFormation(
        stringid=f"fa_{species.stringid}",
        label=f"First Acquisition - {species.label}",
        type=LocationType.firsts,
        species_type=species.stringid,
        water_needed=species.water_needed,
        fence_grade=species.fence_grade
    ))
    locations.append(LocationFormation(
        stringid=f"cr_{species.stringid}",
        label=f"Conservation Release - {species.label}",
        type=LocationType.conservation,
        species_type=species.stringid,
        water_needed=species.water_needed,
        fence_grade=species.fence_grade
    ))

    return locations


with open("ArchipelagoPZ\worlds\planetzoo\data\specieses.json") as json_file:
    json_data = json.load(json_file)
    lfl = [SpeciesesFormation.model_validate(
        loopstuff)for loopstuff in json_data]
    # location formation list

    locations: list[LocationFormation] = []
    for species in lfl:
        locations.extend(species_to_locations(species))
    with open("ArchipelagoPZ\worlds\planetzoo\data\\specieslocations.json", "+w") as output_file:
        json.dump([l.model_dump()for l in locations], output_file)
