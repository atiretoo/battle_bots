"""
Top cover / carapace for the antweight BattleBot (inspired by 'The Twins').
Features:
- Faceted aerodynamic carapace profile
- Stylized debossed 'sleepy eyes' tribute to The Twins
- Central vertical spinner pass-through clearance slot
- Countersunk mounting holes aligning with chassis pillars
"""

import cadquery as cq
try:
    from src.params import *
except ImportError:
    from params import *


def create_cover() -> cq.Workplane:
    """
    Builds the top cover shell with stylized eyes, spinner slot, and mounting holes.
    """
    total_w = ROBOT_WIDTH          # 136 mm
    total_l = MAIN_BODY_LENGTH      # 82 mm
    cover_h = 10.0                  # Height of the cover carapace
    chassis_top_z = CHASSIS_BOTTOM_Z + CHASSIS_HEIGHT  # 35.5 mm
    
    # -------------------------------------------------------------------------
    # 1. Base Cover Block
    # -------------------------------------------------------------------------
    cover = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z)
        .rect(total_w, total_l)
        .extrude(cover_h)
    )
    
    # Chamfer outer vertical corners to match chassis
    cover = cover.edges("|Z").chamfer(6.0)
    
    # Chamfer top perimeter for faceted carapace look
    cover = cover.edges(">Z and |X").chamfer(4.0)
    cover = cover.edges(">Z and |Y").chamfer(3.0)
    
    # -------------------------------------------------------------------------
    # 2. Hollow Underbelly (Leaves clearance for electronics/wiring)
    # -------------------------------------------------------------------------
    inner_cut = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z - 1.0)
        .rect(total_w - 2 * 3.0, total_l - 2 * 3.0)
        .extrude(cover_h - 2.5 + 1.0)
    )
    cover = cover.cut(inner_cut)
    
    # -------------------------------------------------------------------------
    # 3. Central Spinner Slot
    # -------------------------------------------------------------------------
    slot_w = WEAPON_SLOT_WIDTH + 4.0  # 16 mm wide
    # Slot from front edge Y = +41 down towards Y = +10
    spinner_slot = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z - 2.0)
        .transformed(offset=(0, 26.0, 0))
        .rect(slot_w, 32.0)
        .extrude(cover_h + 5.0)
    )
    cover = cover.cut(spinner_slot)
    
    # -------------------------------------------------------------------------
    # 4. Stylized 'Sleepy Eyes' (The Twins Signature Feature)
    # -------------------------------------------------------------------------
    # Debossed 1mm into top-front surface for dual-color printing or painting
    eye_x = 24.0
    eye_y = 20.0
    eye_w = 16.0
    eye_h = 10.0
    deboss_depth = 1.0
    
    # Left eye outline
    left_eye = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z + cover_h - deboss_depth)
        .transformed(offset=(-eye_x, eye_y, 0))
        .rect(eye_w, eye_h)
        .extrude(deboss_depth + 1.0)
    )
    
    # Right eye outline
    right_eye = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z + cover_h - deboss_depth)
        .transformed(offset=(eye_x, eye_y, 0))
        .rect(eye_w, eye_h)
        .extrude(deboss_depth + 1.0)
    )
    
    # Eye lids (slanted sleepy brows)
    lid_h = 4.5
    left_lid = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z + cover_h - deboss_depth)
        .transformed(offset=(-eye_x, eye_y + 2.5, 0), rotate=(0, 0, -10))
        .rect(eye_w + 2.0, lid_h)
        .extrude(deboss_depth)
    )
    right_lid = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z + cover_h - deboss_depth)
        .transformed(offset=(eye_x, eye_y + 2.5, 0), rotate=(0, 0, 10))
        .rect(eye_w + 2.0, lid_h)
        .extrude(deboss_depth)
    )
    
    cover = cover.cut(left_eye).cut(right_eye)
    cover = cover.union(left_lid).union(right_lid)
    
    # -------------------------------------------------------------------------
    # 5. Mounting Holes (M3 countersunk to match chassis pillars)
    # -------------------------------------------------------------------------
    boss_x = 42.0
    boss_y = 32.0
    mount_locs = [
        (-boss_x, -boss_y),
        (boss_x, -boss_y),
        (-boss_x, boss_y),
        (boss_x, boss_y),
    ]
    
    # Through holes for M3 screws
    mount_holes = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z - 2.0)
        .pushPoints(mount_locs)
        .circle(SCREW_M3_CLEAR_DIA / 2.0)
        .extrude(cover_h + 5.0)
    )
    # Countersink recess for screw heads
    countersinks = (
        cq.Workplane("XY")
        .workplane(offset=chassis_top_z + cover_h - 2.5)
        .pushPoints(mount_locs)
        .circle(6.0 / 2.0)
        .extrude(3.0)
    )
    
    cover = cover.cut(mount_holes).cut(countersinks)
    
    return cover


if __name__ == "__main__":
    result = create_cover()
