"""
Front wedge component for the antweight BattleBot (inspired by 'The Twins').
Features:
- Low-angle forward sloped ramp
- Extended front ground forks / feeder teeth
- Central clearance slot for the vertical spinner
- Secure mounting points to attach to the main chassis
"""

import cadquery as cq
try:
    from src.params import *
except ImportError:
    from params import *


def create_wedge() -> cq.Workplane:
    """
    Builds the front wedge with integrated forks and spinner slot.
    """
    wedge_w = ROBOT_WIDTH           # 136 mm
    chassis_front_y = MAIN_BODY_LENGTH / 2.0  # +41.0 mm
    wedge_reach_y = 36.0            # Extends from Y=41 to Y=77 mm
    tip_y = chassis_front_y + wedge_reach_y   # 77.0 mm
    
    ramp_top_z = CHASSIS_BOTTOM_Z + CHASSIS_HEIGHT  # 35.5 mm
    ramp_bot_z = 1.0                # Ground scraper edge
    
    # -------------------------------------------------------------------------
    # 1. Main Wedge Profile (Extruded along X)
    # -------------------------------------------------------------------------
    # In the YZ plane:
    # (Y=chassis_front_y, Z=CHASSIS_BOTTOM_Z) -> (Y=tip_y, Z=ramp_bot_z) ->
    # (Y=tip_y - 3, Z=ramp_bot_z + 4) -> (Y=chassis_front_y, Z=ramp_top_z) -> close
    # Using 'ZX' workplane or 'YZ' workplane:
    # On 'YZ', local X is Y, local Y is Z.
    
    wedge_profile = (
        cq.Workplane("YZ")
        .workplane(offset=-wedge_w / 2.0)
        .moveTo(chassis_front_y, CHASSIS_BOTTOM_Z)
        .lineTo(tip_y, ramp_bot_z)
        .lineTo(tip_y, ramp_bot_z + 3.0)
        .lineTo(chassis_front_y, ramp_top_z)
        .close()
        .extrude(wedge_w)
    )
    
    # Chamfer side edges of the wedge to match the chassis profile
    wedge = wedge_profile.edges("|Z").chamfer(6.0)
    
    # -------------------------------------------------------------------------
    # 2. Central Vertical Spinner Pass-Through Slot
    # -------------------------------------------------------------------------
    slot_w = WEAPON_SLOT_WIDTH + 4.0  # 16 mm wide
    spinner_slot = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .rect(slot_w, wedge_reach_y * 2.0)
        .extrude(ramp_top_z + 10.0)
        .translate((0, chassis_front_y + wedge_reach_y / 2.0, 0))
    )
    wedge = wedge.cut(spinner_slot)
    
    # -------------------------------------------------------------------------
    # 3. Ground Scraping Forks (The Twins Signature Feature)
    # -------------------------------------------------------------------------
    # Two long ground-feeder prongs extending forward from the wedge
    fork_length = 28.0
    fork_w = 7.0
    fork_h = 6.0
    fork_x = 30.0  # Distance from centerline
    
    fork_left = (
        cq.Workplane("XY")
        .workplane(offset=ramp_bot_z)
        .transformed(offset=(-fork_x, tip_y - 8.0, 0))
        .rect(fork_w, fork_length)
        .extrude(fork_h)
        .edges(">Y and >Z").chamfer(3.0)
    )
    
    fork_right = (
        cq.Workplane("XY")
        .workplane(offset=ramp_bot_z)
        .transformed(offset=(fork_x, tip_y - 8.0, 0))
        .rect(fork_w, fork_length)
        .extrude(fork_h)
        .edges(">Y and >Z").chamfer(3.0)
    )
    
    wedge = wedge.union(fork_left).union(fork_right)
    
    # -------------------------------------------------------------------------
    # 4. Mounting Tongue & Fastener Holes
    # -------------------------------------------------------------------------
    # Tongue that inserts slightly under the chassis front for solid rigidity
    tongue_w = 50.0
    tongue_l = 10.0
    tongue_th = FLOOR_THICKNESS
    
    tongue = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z)
        .transformed(offset=(0, chassis_front_y - tongue_l / 2.0, 0))
        .rect(tongue_w, tongue_l)
        .extrude(tongue_th)
    )
    
    # Screw holes matching the chassis front bosses
    mount_holes = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .pushPoints([(-20.0, chassis_front_y - 4.0), (20.0, chassis_front_y - 4.0)])
        .circle(SCREW_M3_CLEAR_DIA / 2.0)
        .extrude(ramp_top_z)
    )
    
    wedge = wedge.union(tongue).cut(mount_holes)
    
    return wedge


if __name__ == "__main__":
    result = create_wedge()
