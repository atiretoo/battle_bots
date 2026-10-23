"""
Parameter definitions for the antweight BattleBot (inspired by 'The Twins').
All dimensions in millimeters (mm).

Coordinate system convention:
  +X : Right
  -X : Left
  +Y : Front (forward drive)
  -Y : Rear (reverse drive)
  +Z : Up
  Z=0: Ground plane (wheels contact at Z=0)
"""

# -----------------------------------------------------------------------------
# Wheel & Drive Geometry
# -----------------------------------------------------------------------------
WHEEL_DIAMETER = 44.0       # Diameter of drive wheels
WHEEL_RADIUS = WHEEL_DIAMETER / 2.0  # 22.0 mm
WHEEL_WIDTH = 12.0          # Width of wheel tire
WHEEL_CLEARANCE = 2.5       # Radial clearance inside wheel well
WHEEL_WELL_WIDTH = WHEEL_WIDTH + 2 * 2.0  # Clearance along axle

GROUND_CLEARANCE = 3.5      # Chassis bottom clearance off the ground
AXLE_Z = WHEEL_RADIUS       # Axle height = 22.0 mm above ground
CHASSIS_BOTTOM_Z = GROUND_CLEARANCE  # 3.5 mm

# -----------------------------------------------------------------------------
# TT Motor Specifications (from assets/TT Motor.step)
# -----------------------------------------------------------------------------
TT_BODY_WIDTH = 22.5        # Across motor body (X-dim in raw step)
TT_BODY_LENGTH = 70.2       # Overall length from can rear to gearbox tip
TT_BODY_THICKNESS = 18.8    # Motor body thickness
TT_AXLE_OFFSET_FRONT = 16.2 # Distance from axle center to front gearbox tip
TT_AXLE_OFFSET_REAR = 54.0  # Distance from axle center to rear motor terminals
TT_AXLE_DIAMETER = 5.4      # Dual-flat output shaft diameter
TT_AXLE_PROTRUSION = 9.0    # Shaft protrusion from gearbox face
TT_MOUNT_HOLE_SPACING = 34.4 # Spacing between M3 mounting through-holes
TT_MOUNT_HOLE_DIA = 3.2     # Clearance for M3 screw

# -----------------------------------------------------------------------------
# Chassis Overall Dimensions
# -----------------------------------------------------------------------------
WALL_THICKNESS = 2.4        # Standard rigid 3D printed shell wall thickness
FLOOR_THICKNESS = 2.0       # Chassis bottom plate thickness
ROBOT_WIDTH = 136.0         # Total width including outer wheel armor
MAIN_BODY_LENGTH = 82.0     # Length of the main chassis tub
CHASSIS_HEIGHT = 32.0       # Height of the main chassis tub

# Wheel positions (centered on axle Y = 0)
AXLE_Y = 0.0
WHEEL_TRACK = 112.0         # Center-to-center distance between left and right wheels
WHEEL_X_OFFSET = WHEEL_TRACK / 2.0  # 56.0 mm

# Motor placement:
# Left motor placed at negative X, Right motor placed at positive X
# Axles aligned transversely with Global X.
MOTOR_SPACING_X = 26.0      # Center-to-center gap between the two motor inner faces

# -----------------------------------------------------------------------------
# Electronics Bays (Dimensions in mm)
# -----------------------------------------------------------------------------
# 9V Rechargeable Li-ion battery (PP3 form factor)
BATTERY_LENGTH = 49.0
BATTERY_WIDTH = 27.0
BATTERY_HEIGHT = 18.0

# Arduino Nano / Pro Mini
ARDUINO_LENGTH = 45.0
ARDUINO_WIDTH = 18.5
ARDUINO_HEIGHT = 10.0

# Dual H-Bridge (e.g. MX1508 or DRV8833 breakout)
HBRIDGE_LENGTH = 26.0
HBRIDGE_WIDTH = 22.0
HBRIDGE_HEIGHT = 8.0

# 2.4 GHz ELRS Receiver
ELRS_LENGTH = 18.0
ELRS_WIDTH = 12.0
ELRS_HEIGHT = 5.0

# -----------------------------------------------------------------------------
# Weapon System (Vertical Spinner)
# -----------------------------------------------------------------------------
# 130/180-size high-speed DC motor
WEAPON_MOTOR_DIA = 20.4
WEAPON_MOTOR_LENGTH = 28.0
WEAPON_MOTOR_FLAT = 15.4

# Spinner Disc
WEAPON_DISC_DIA = 48.0      # Spinner diameter
WEAPON_DISC_THICKNESS = 4.0 # 3D printed disc thickness
WEAPON_TOOTH_REACH = 4.0    # Single or double bite tooth height
WEAPON_SLOT_WIDTH = 12.0    # Wedge/cover pass-through slot width

# -----------------------------------------------------------------------------
# Fastener & Tolerances
# -----------------------------------------------------------------------------
SCREW_M3_TAP_DIA = 2.8      # Direct-tap M3 hole in printed plastic
SCREW_M3_CLEAR_DIA = 3.3    # Clearance hole for M3 screw
SCREW_M2_TAP_DIA = 1.8      # Direct-tap M2 hole
PRINTER_TOLERANCE = 0.3     # Fit clearance for mating parts
