# BattleBots CAD Project

This repository contains parametric 3D CAD models and assemblies for combat robots (BattleBots), built using [CadQuery](https://github.com/CadQuery/cadquery).

## Modeling Guidelines & Best Practices

When designing parts and assemblies in this project:

- **BRep over CSG**: Prioritize Boundary Representation modeling (selecting faces/edges and applying features such as extrude, hole, fillet, shell) over pure CSG boolean operations (`union`, `cut`) to maintain robust, parametric geometry.
- **Coordinate Systems & Workplanes**:
  - Remember the right-hand cyclic order ($X \rightarrow Y \rightarrow Z \rightarrow X$).
  - Planes `"XY"`, `"YZ"`, and `"ZX"` have $+Z$, $+X$, and $+Y$ normal vectors respectively.
  - Avoid `"XZ"` if positive $+Y$ extrusion is expected; use `"ZX"` instead (where local coordinates map as $(z, x)$) or select faces directly with `.faces(">Y").workplane()`.
- **Selectors**:
  - Prefer stable geometric selectors (`>Z`, `<Z`, `|X`, etc.) and tagging (`.tag("name")`) over fragile numeric indices (`>>Z[0]`).
  - Explicitly specify `centerOption` (e.g. `CenterOfBoundBox` or `ProjectedOrigin`) when face centering behavior is critical.
