"""
Vertical spinner weapon disc for the antweight BattleBot.
Features:
- Single-tooth high-bite combat geometry with dynamic counterweight balance
- Central motor shaft bore (2.0mm standard DC motor shaft) with flat D-bore option
- 3D printable in tough PLA, PETG, or Nylon
"""

import cadquery as cq
try:
    from src.params import *
except ImportError:
    from params import *


def create_weapon_disc() -> cq.Workplane:
    """
    Builds the vertical spinner disc.
    Disc is oriented on the YZ plane so it sits vertically along the robot centerline (X=0).
    """
    r = WEAPON_DISC_DIA / 2.0       # 24.0 mm
    th = WEAPON_DISC_THICKNESS       # 4.0 mm
    tooth_h = WEAPON_TOOTH_REACH     # 4.0 mm
    bore_r = 1.0                     # 2.0 mm shaft diameter (130/180 motor)
    
    # -------------------------------------------------------------------------
    # 1. Base Disc Blank on YZ plane (Vertical spinner orientation)
    # -------------------------------------------------------------------------
    disc = (
        cq.Workplane("YZ")
        .workplane(offset=-th / 2.0)
        .circle(r)
        .extrude(th)
    )
    
    # -------------------------------------------------------------------------
    # 2. Add Asymmetric Impact Tooth
    # -------------------------------------------------------------------------
    # Impact tooth on top (+Z) providing high bite
    tooth = (
        cq.Workplane("YZ")
        .workplane(offset=-th / 2.0)
        .moveTo(0, r - 2.0)
        .lineTo(8.0, r + tooth_h)
        .lineTo(0, r + tooth_h)
        .lineTo(-12.0, r - 2.0)
        .close()
        .extrude(th)
    )
    disc = disc.union(tooth)
    
    # -------------------------------------------------------------------------
    # 3. Dynamic Balance Cutout
    # -------------------------------------------------------------------------
    # Teardrop balance hole on the opposite quadrant to counterbalance the tooth
    balance_hole = (
        cq.Workplane("YZ")
        .workplane(offset=-th / 2.0 - 1.0)
        .transformed(offset=(0, -r / 2.0, 0))
        .circle(6.0)
        .extrude(th + 2.0)
    )
    disc = disc.cut(balance_hole)
    
    # -------------------------------------------------------------------------
    # 4. Center Shaft Bore with D-flat
    # -------------------------------------------------------------------------
    # 2mm shaft hole with 1.6mm flat for positive torque transmission
    shaft_bore = (
        cq.Workplane("YZ")
        .workplane(offset=-th / 2.0 - 1.0)
        .circle(bore_r)
        .extrude(th + 2.0)
    )
    disc = disc.cut(shaft_bore)
    
    # Chamfer perimeter edges for strength
    disc = disc.edges("|X and >Z").fillet(0.8)
    
    return disc


if __name__ == "__main__":
    result = create_weapon_disc()
