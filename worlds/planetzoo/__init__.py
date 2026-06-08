#*B1 — Skeleton APWorld**
#-Scaffold the World subclass; build `item_name_to_id` / `location_name_to_id` from `data.json`;
# declare options + game name; generate a seed without crashing.
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md
# Rules are included here

from .World import PlanetZooWorld as PlanetZooWorld



# # from that group has been collected. Group names can also be used for !hint
# item_name_groups = {
#     "species": {
#         "Permit: Saltwater Crocodile",
#         "Permit: Western Lowland Gorilla",
#         "Permit: Giant Panda"
#         },
#     "climate": {
#         "Climate Control: Tropical",
#         "Climate Control : Cold",
#         "Water Habitat Tools"
#         },
#     "buildings": {
#         "Research Centre",
#         "Veterinary Surgery"
#         },
#     "research":{
#         "Research Welfare - Plains Zebra",
#         "Research Welfare - Grey Wolf",
#         "Research Welfare - American Bison",
#         "Research Welfare - Bengal Tiger",
#         "Research Welfare - African Elephant",
#         "Research Welfare - Nile Hippopotamus",
#         "Research Welfare - Saltwater Crocodile",
#         "Research Welfare - Snow Leopard",
#         "Research Welfare - Western Lowland Gorilla",
#         "Research Welfare - Giant Panda",
#         "Research Enrichment - Generalist Toys",
#         "Research Habitat - Advanced Barriers"
#         }
# }


# def create_regions(self) -> None:
#     """Creating independent Regions"""
#     regions_by_name = {}
#     print("Region creation being triggered")
#     for region_info in self.all_regions: 
#         region = Region(region_info.name, self.player, self.multiworld)
#         regions_by_name[region_info.name] = region
#         for location_name in region_info.locations:
#             location = PlanetZooLocation(self.player, location_name, self.location_name_to_id.get(location_name, None), region)
#             region.locations.append(location)
#         self.multiworld.regions.append(region)



# def fill_slot_data(self) -> dict:
#     returndict = {
#         "starting_money" : self.options.starting_money.value
#     }
#     return returndict
    
# # if PlanetZooWorld.options.starting_species:
# #     starting_species = PlanetZooWorld.create_item("Starting Species")
# #     PlanetZooWorld.push_precollected(starting_species)