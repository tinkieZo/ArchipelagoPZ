from __future__ import annotations
from typing import TYPE_CHECKING
from rule_builder.rules import Has, HasAll, CanReachLocation
from .Items import ItemNames
from .Names import EntranceNames
from .Locations import LocationNames
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from .World import PlanetZooWorld



HAS_CENTRE = Has(ItemNames.research_centre)
HAS_WORKSHOP = Has(ItemNames.workshop)
    

#Current Problem
def set_all_rules(world: PlanetZooWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

#Research and Mechanics require buildings to be accessible
def set_all_entrance_rules(world: PlanetZooWorld) -> None:
    menu_to_research = world.multiworld.get_entrance(EntranceNames.menu_to_research, world.player)
    world.set_rule(menu_to_research, HAS_CENTRE)

    menu_to_mechanic = world.multiworld.get_entrance(EntranceNames.menu_to_mechanic, world.player)
    world.set_rule(menu_to_mechanic, HAS_WORKSHOP)


#Logic graph integrated here?
def set_all_location_rules(world: PlanetZooWorld) -> None:
    #Animals that area gated rules are here
    #Permits for seperate animals

    HAS_PERMIT_HIPPO = Has(ItemNames.water_hab_tools)
    hippo_permit = world.multiworld.get_location(LocationNames.rw_nile_hippo, world.player)
    world.set_rule(hippo_permit, HAS_PERMIT_HIPPO)

    HAS_PERMIT_SALTCROC = HasAll(ItemNames.permit_saltwater_croc, ItemNames.water_hab_tools)
    saltcroc_permit = world.multiworld.get_location(LocationNames.rw_saltwater_croc, world.player)
    world.set_rule(saltcroc_permit, HAS_PERMIT_SALTCROC)

    HAS_PERMIT_WLGORILLA = Has(ItemNames.permit_w_l_gorilla)
    gorilla_permit_fb = world.multiworld.get_location(LocationNames.fb_w_l_gorilla, world.player)
    gorilla_permit_rw = world.multiworld.get_location(LocationNames.rw_w_l_gorilla, world.player)
    world.set_rule(gorilla_permit_fb, HAS_PERMIT_WLGORILLA)
    world.set_rule(gorilla_permit_rw, HAS_PERMIT_WLGORILLA)

    HAS_PERMIT_BTIGER = Has(ItemNames.permit_bengal_tiger)
    bengal_permit_fb = world.multiworld.get_location(LocationNames.fb_bengal_tiger, world.player)
    bengal_permit_rw = world.multiworld.get_location(LocationNames.rw_bengal_tiger, world.player)
    world.set_rule(bengal_permit_fb, HAS_PERMIT_BTIGER)
    world.set_rule(bengal_permit_rw, HAS_PERMIT_BTIGER)

    HAS_PERMIT_SLEOPARD = Has(ItemNames.permit_snow_leopard)
    leopard_permit = world.multiworld.get_location(LocationNames.rw_snow_leopard, world.player)
    world.set_rule(leopard_permit, HAS_PERMIT_SLEOPARD)

    HAS_GIANTPPERMIT = Has(ItemNames.permit_giant_panda)
    panda_permit_fb = world.multiworld.get_location(LocationNames.fb_giant_panda, world.player)
    panda_permit_rw = world.multiworld.get_location(LocationNames.rw_giant_panda, world.player)
    world.set_rule(panda_permit_fb, HAS_GIANTPPERMIT)
    world.set_rule(panda_permit_rw, HAS_GIANTPPERMIT)

   
    #Need to release at least one animal to unlock Conservation Program
    HAS_CONS_PROG = Has(ItemNames.conserve_program)
    cons_program = world.multiworld.get_location(LocationNames.ms_first_conserv_release, world.player)
    world.set_rule(cons_program, HAS_CONS_PROG)



HAS_FLAGSHIP = HasAll(ItemNames.conserve_program, ItemNames.permit_giant_panda)

def set_completion_condition(world: PlanetZooWorld) -> None:
     world.set_completion_rule(HAS_FLAGSHIP)
    #  world.set_completion_rule(Has("Goal"))