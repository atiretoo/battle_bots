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

## Development & AI Policy: The "Centaur" Approach

This project is developed using a collaborative human-AI workflow. The code, architecture, and documentation were written and refined with the assistance of advanced AI models. 

I approach AI not as a tool for blind self-automation, but as a collaborative interaction. I aspire to be a [centaur](https://mitsloan.mit.edu/ideas-made-to-matter/3-ways-to-use-ai-are-you-a-cyborg-a-centaur-or-a-self-automator), "... maintain[ing] structured and controlled interactions with AI, harnessing it as a tool for targeted efficiency". I acknowledge that when learning a new domain I might be a cyborg "... collaborat[ing] closely with the AI tool -- probing its suggestions, allowing it to lead the way, and taking its advice on some occasions while pushing back against it on others." Both are OK. In this model, the AI acts as a high-powered pair-programming partner. It helps me rapidly explore and develop my own understanding of complex topics. Meanwhile, I hold the strategic vision, conduct the physical testing/validation, and apply and build domain knowledge as I go.

For rules regarding AI-assisted contributions from the community, please see the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project utilizes a **Dual License** structure to comply with both software and open-source hardware best practices. These specific open-source licenses were chosen to support the transition to an anarchist economy—promoting mutual aid, free distribution of information, and breaking down artificial scarcity.

*   **Software (Python Code):** All source code in this repository is licensed under the [GNU Affero General Public License v3.0 (AGPLv3)](COPYING). This ensures that any modifications to the code remain open-source and provides explicit patent protections.
*   **Hardware (3D Models):** The generated output files (STL and STEP files) are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](LICENSE). This is the standard license for the 3D printing community.
