"""
Drive wheel for the antweight BattleBot.
Designed to press-fit onto standard yellow TT gearmotor dual-flat output shafts.
Includes rim grooves for O-rings / rubber tires or direct printing in TPU.
"""

import cadquery as cq
try:
    from src.params import *
except ImportError:
    from params import *


def create_wheel() -> cq.Workplane:
    """
    Builds a 44mm drive wheel with TT motor shaft coupler and tire traction grooves.
    Oriented on the YZ plane (axle along X).
    """
    r = WHEEL_RADIUS            # 22.0 mm
    w = WHEEL_WIDTH             # 12.0 mm
    hub_r = 7.0                 # 14mm central hub
    bore_r = 2.7                # 5.4 mm shaft diameter
    flat_w = 3.7                # Distance across the two flats
    
    # -------------------------------------------------------------------------
    # 1. Main Wheel Rim & Hub
    # -------------------------------------------------------------------------
    wheel = (
        cq.Workplane("YZ")
        .circle(r)
        .extrude(w)
    )
    
    # Lightening recess between hub and outer rim
    recess = (
        cq.Workplane("YZ")
        .workplane(offset=2.5)
        .circle(r - 3.0)
        .circle(hub_r + 2.0)
        .extrude(w - 2.5 + 1.0)
    )
    wheel = wheel.cut(recess)
    
    # -------------------------------------------------------------------------
    # 2. TT Motor Dual-Flat Shaft Socket
    # -------------------------------------------------------------------------
    # The standard TT shaft is a 5.4mm cylinder with two parallel flats 3.7mm apart
    shaft_hole = (
        cq.Workplane("YZ")
        .workplane(offset=-1.0)
        .circle(bore_r)
        .extrude(w + 2.0)
    )
    # The two flats cut away into the bore from both sides
    flat_cutter = (
        cq.Workplane("YZ")
        .workplane(offset=-1.0)
        .rect(flat_w, bore_r * 4.0)
        .extrude(w + 2.0)
    )
    # The D-hole is the intersection of the circle and the rectangle
    d_hole = shaft_hole.intersect(flat_cutter)
    wheel = wheel.cut(d_hole)
    
    # -------------------------------------------------------------------------
    # 3. Tire Traction Grooves
    # -------------------------------------------------------------------------
    # Circumferential grooves on outer tread for O-rings or TPU grip
    groove_1 = (
        cq.Workplane("YZ")
        .workplane(offset=3.0)
        .circle(r + 1.0)
        .circle(r - 1.2)
        .extrude(2.0)
    )
    groove_2 = (
        cq.Workplane("YZ")
        .workplane(offset=7.0)
        .circle(r + 1.0)
        .circle(r - 1.2)
        .extrude(2.0)
    )
    wheel = wheel.cut(groove_1).cut(groove_2)
    
    # Bevel outer rim edge
    wheel = wheel.edges(">X and %Circle").fillet(0.8)
    
    return wheel


if __name__ == "__main__":
    result = create_wheel()
