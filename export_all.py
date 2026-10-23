"""
Export script for the antweight BattleBot.
Generates 3D printable STL files and STEP assemblies into the exports/ folder.
"""

import os
import cadquery as cq
from src.params import *
from src.chassis import create_chassis
from src.wedge import create_wedge
from src.cover import create_cover
from src.weapon import create_weapon_disc
from src.wheel import create_wheel
from src.assembly import create_full_assembly


def export_all():
    export_dir = os.path.join(os.path.dirname(__file__), "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    parts = {
        "chassis.stl": create_chassis(),
        "front_wedge.stl": create_wedge(),
        "cover.stl": create_cover(),
        "weapon_disc.stl": create_weapon_disc(),
        "wheel.stl": create_wheel(),
    }
    
    print("Exporting STL files for 3D printing...")
    for filename, part in parts.items():
        out_path = os.path.join(export_dir, filename)
        cq.exporters.export(part, out_path, cq.exporters.ExportTypes.STL, tolerance=0.05, angularTolerance=0.1)
        print(f"  -> Exported: {filename}")
        
    print("Exporting full assembly STEP file...")
    assy = create_full_assembly()
    step_path = os.path.join(export_dir, "battle_bot_assembly.step")
    assy.save(step_path)
    print(f"  -> Exported: battle_bot_assembly.step")
    print("Done! All models ready in exports/")


if __name__ == "__main__":
    export_all()
