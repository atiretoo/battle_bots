"""
Full assembly for the antweight BattleBot (inspired by 'The Twins').
Combines:
- Main Chassis (white)
- Front Wedge with ground forks (charcoal)
- Top Carapace Cover with sleepy eyes (purple/magenta)
- Vertical Spinner Disc (red/steel)
- Drive Wheels (black)
- TT Gearmotors (yellow)
"""

import os
import cadquery as cq
try:
    from src.params import *
    from src.chassis import create_chassis
    from src.wedge import create_wedge
    from src.cover import create_cover
    from src.weapon import create_weapon_disc
    from src.wheel import create_wheel
except ImportError:
    from params import *
    from chassis import create_chassis
    from wedge import create_wedge
    from cover import create_cover
    from weapon import create_weapon_disc
    from wheel import create_wheel


def load_tt_motor() -> cq.Workplane:
    """Loads and combines all solids from assets/TT Motor.step."""
    step_path = os.path.join(os.path.dirname(__file__), "..", "assets", "TT Motor.step")
    if not os.path.exists(step_path):
        step_path = "assets/TT Motor.step"
    imported = cq.importers.importStep(step_path)
    compound = cq.Compound.makeCompound(imported.solids().vals())
    return cq.Workplane().add(compound)


def create_full_assembly() -> cq.Assembly:
    """Builds and returns the full colored CadQuery assembly."""
    assy = cq.Assembly(name="TheTwins_BattleBot")
    
    # 1. Main Chassis
    chassis = create_chassis()
    assy.add(chassis, name="Chassis", color=cq.Color(0.92, 0.92, 0.94, 1.0))
    
    # 2. Front Wedge with scraping forks
    wedge = create_wedge()
    assy.add(wedge, name="FrontWedge", color=cq.Color(0.22, 0.22, 0.24, 1.0))
    
    # 3. Top Cover Carapace
    cover = create_cover()
    assy.add(cover, name="TopCover", color=cq.Color(0.60, 0.15, 0.55, 1.0))
    
    # 4. Vertical Spinner Disc
    weapon_disc = create_weapon_disc()
    weapon_loc = cq.Location(cq.Vector(0, 38.0, 26.0))
    assy.add(weapon_disc, name="WeaponDisc", loc=weapon_loc, color=cq.Color(0.85, 0.15, 0.15, 1.0))
    
    # 5. Wheels
    wheel_l = create_wheel()
    wheel_r = create_wheel()
    # Left wheel: center of wheel well at X = -56 mm, Y = 0, Z = AXLE_Z (22 mm)
    loc_wheel_l = cq.Location(cq.Vector(-WHEEL_X_OFFSET - WHEEL_WIDTH / 2.0, 0, AXLE_Z))
    # Right wheel: center of wheel well at X = +56 mm
    loc_wheel_r = cq.Location(cq.Vector(WHEEL_X_OFFSET - WHEEL_WIDTH / 2.0, 0, AXLE_Z))
    assy.add(wheel_l, name="Wheel_Left", loc=loc_wheel_l, color=cq.Color(0.15, 0.15, 0.15, 1.0))
    assy.add(wheel_r, name="Wheel_Right", loc=loc_wheel_r, color=cq.Color(0.15, 0.15, 0.15, 1.0))
    
    # 6. TT Gearmotors
    try:
        motor = load_tt_motor()
        # In STEP: axle is along Z, length along Y (-54 to +16.2), body thickness along X.
        # Rotating -90 around Y aligns Z (axle) with +X.
        motor_rot = motor.rotate((0, 0, 0), (0, 1, 0), -90)
        
        # Left motor: shaft points left (-X) -> rotate 180 around Z
        motor_left = motor_rot.rotate((0, 0, 0), (0, 0, 1), 180)
        loc_motor_l = cq.Location(cq.Vector(-32.5, 0, AXLE_Z))
        assy.add(motor_left, name="Motor_Left", loc=loc_motor_l, color=cq.Color(0.95, 0.75, 0.10, 1.0))
        
        # Right motor: shaft points right (+X)
        loc_motor_r = cq.Location(cq.Vector(32.5, 0, AXLE_Z))
        assy.add(motor_rot, name="Motor_Right", loc=loc_motor_r, color=cq.Color(0.95, 0.75, 0.10, 1.0))
    except Exception as e:
        print(f"Note: TT Motor STEP model could not be loaded into assembly: {e}")
        
    return assy


if __name__ == "__main__":
    result = create_full_assembly()
