"""
Main chassis for the antweight BattleBot.
Houses two TT motors, provides enclosed wheel wells, and contains electronics bays.
"""

import cadquery as cq
try:
    from src.params import *
except ImportError:
    from params import *


def create_chassis() -> cq.Workplane:
    """
    Builds the main chassis body with:
    - Integrated motor cradles for two TT gearmotors
    - Fully shielded outer wheel wells
    - Central electronics and battery compartment
    - Mounting posts for front wedge and top cover
    """
    # -------------------------------------------------------------------------
    # 1. Base Outer Shell Block
    # -------------------------------------------------------------------------
    # The base envelope spans across the outer wheel armor pods.
    # Center is at X=0, Y=0 (axle center), Z=CHASSIS_BOTTOM_Z to CHASSIS_BOTTOM_Z + CHASSIS_HEIGHT
    
    total_w = ROBOT_WIDTH          # 136 mm
    total_l = MAIN_BODY_LENGTH      # 82 mm
    total_h = CHASSIS_HEIGHT        # 32 mm
    
    # We construct the base solid on the XY plane, elevated to CHASSIS_BOTTOM_Z
    base = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z)
        .rect(total_w, total_l)
        .extrude(total_h)
    )
    
    # Chamfer outer vertical corners for sleek deflection angles (anti-spinner)
    base = base.edges("|Z").chamfer(6.0)
    
    # -------------------------------------------------------------------------
    # 2. Wheel Wells (Cutouts for Drive Wheels)
    # -------------------------------------------------------------------------
    # Wheels are at X = ±WHEEL_X_OFFSET (±56mm), Y = 0, Z = AXLE_Z (22mm)
    # The wheel well removes material from the bottom so the wheel reaches ground.
    ww_rad = WHEEL_RADIUS + WHEEL_CLEARANCE  # 22 + 2.5 = 24.5 mm
    ww_width = WHEEL_WELL_WIDTH              # 16 mm
    
    # Left wheel well cylinder along X
    left_ww = (
        cq.Workplane("YZ")
        .workplane(offset=-WHEEL_X_OFFSET - ww_width / 2.0)
        .circle(ww_rad)
        .extrude(ww_width)
    )
    # Also open the bottom of the wheel well down through the floor
    left_ww_slot = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .transformed(offset=(-WHEEL_X_OFFSET, 0, 0))
        .rect(ww_width, ww_rad * 2.0)
        .extrude(AXLE_Z)
    )
    
    # Right wheel well cylinder along X
    right_ww = (
        cq.Workplane("YZ")
        .workplane(offset=WHEEL_X_OFFSET - ww_width / 2.0)
        .circle(ww_rad)
        .extrude(ww_width)
    )
    right_ww_slot = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .transformed(offset=(WHEEL_X_OFFSET, 0, 0))
        .rect(ww_width, ww_rad * 2.0)
        .extrude(AXLE_Z)
    )
    
    # -------------------------------------------------------------------------
    # 3. Internal Cavities: Motor Bays & Electronics
    # -------------------------------------------------------------------------
    # Central electronics bay (between motors / front-to-rear)
    center_cavity = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z + FLOOR_THICKNESS)
        .rect(32.0, total_l - 2 * WALL_THICKNESS)
        .extrude(total_h)
    )
    
    # Motor pockets on Left and Right:
    # TT motor body is 22.5 wide, ~71 long.
    # Placed between center cavity and wheel inner bulkhead.
    # Axle center is at Y = 0. Motor extends from Y = -TT_AXLE_OFFSET_REAR (-54) to +TT_AXLE_OFFSET_FRONT (+16.2).
    # Motor X: Left motor center around X = -32.5, Right motor center around X = +32.5
    motor_pocket_w = TT_BODY_WIDTH + 1.0       # 23.5 mm
    motor_pocket_l = TT_BODY_LENGTH + 2.0      # 72.2 mm
    motor_pocket_y = (TT_AXLE_OFFSET_FRONT - TT_AXLE_OFFSET_REAR) / 2.0  # -18.9 mm
    
    left_motor_cavity = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z + FLOOR_THICKNESS)
        .transformed(offset=(-32.5, motor_pocket_y, 0))
        .rect(motor_pocket_w, motor_pocket_l)
        .extrude(total_h)
    )
    
    right_motor_cavity = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z + FLOOR_THICKNESS)
        .transformed(offset=(32.5, motor_pocket_y, 0))
        .rect(motor_pocket_w, motor_pocket_l)
        .extrude(total_h)
    )
    
    # Combine main cuts
    chassis = (
        base
        .cut(left_ww)
        .cut(left_ww_slot)
        .cut(right_ww)
        .cut(right_ww_slot)
        .cut(center_cavity)
        .cut(left_motor_cavity)
        .cut(right_motor_cavity)
    )
    
    # -------------------------------------------------------------------------
    # 4. Axle Pass-Through Holes
    # -------------------------------------------------------------------------
    # Holes in the inner bulkheads for the TT motor output shafts to reach the wheels
    axle_hole_dia = 9.0  # Clearance for TT motor axle boss (dia ~5.4 shaft, 8mm boss)
    axle_holes = (
        cq.Workplane("YZ")
        .workplane(offset=-ROBOT_WIDTH / 2.0)
        .transformed(offset=(AXLE_Y, AXLE_Z, 0))
        .circle(axle_hole_dia / 2.0)
        .extrude(ROBOT_WIDTH)
    )
    
    # Intersect only with the inner bulkheads by cutting through the chassis
    chassis = chassis.cut(axle_holes)
    
    # -------------------------------------------------------------------------
    # 5. Top Cover Mounting Bosses
    # -------------------------------------------------------------------------
    # 4 screw mounting pillars at inner corners to bolt the top cover down
    boss_radius = 4.0
    boss_h = total_h - FLOOR_THICKNESS
    boss_x = 42.0
    boss_y = 32.0
    
    boss_locs = [
        (-boss_x, -boss_y),
        (boss_x, -boss_y),
        (-boss_x, boss_y),
        (boss_x, boss_y),
    ]
    
    bosses = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z + FLOOR_THICKNESS)
        .pushPoints(boss_locs)
        .circle(boss_radius)
        .extrude(boss_h)
    )
    
    # M3 pilot holes in bosses for self-tapping or heat-set inserts
    boss_holes = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z + total_h - 12.0)
        .pushPoints(boss_locs)
        .circle(SCREW_M3_TAP_DIA / 2.0)
        .extrude(13.0)
    )
    
    chassis = chassis.union(bosses).cut(boss_holes)
    
    # -------------------------------------------------------------------------
    # 6. Front Wedge Mounting Tabs
    # -------------------------------------------------------------------------
    # Forward tongue / bracket for mating the front wedge
    wedge_mount_locs = [(-20.0, total_l / 2.0 - 4.0), (20.0, total_l / 2.0 - 4.0)]
    wedge_holes = (
        cq.Workplane("XY")
        .workplane(offset=CHASSIS_BOTTOM_Z)
        .pushPoints(wedge_mount_locs)
        .circle(SCREW_M3_TAP_DIA / 2.0)
        .extrude(total_h)
    )
    chassis = chassis.cut(wedge_holes)
    
    return chassis


if __name__ == "__main__":
    result = create_chassis()
