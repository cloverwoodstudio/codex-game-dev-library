# Character creation

Reviewed: 2026-08-29

A character is a coordinated design across narrative, gameplay, silhouette, movement, voice and production cost.

## Character brief

- role in the player's loop and relationship to player agency
- desire, need, fear, contradiction, history and change
- gameplay abilities, constraints, hitbox and readability needs
- silhouette, shape language, palette, materials and scale
- facial/body expressiveness and required animation set
- voice, vocabulary, conversational limits
- variants, equipment, damage states and customization
- representation/sensitivity questions
- production budgets: topology, bones, materials, textures, LODs

## 3D production path

Reference sheet → blockout → high-poly/sculpt if needed → game-ready topology → UVs → bake maps → texture/material → skeleton → skin weights → facial solution → animation set → engine import → gameplay/collision setup → LODs → deformation and performance QA.

Test characters in extreme poses, gameplay camera distance, harsh lighting, crowds and target hardware. The beauty render is not the acceptance test.

Primary starting points:

- Blender animation/rigging: https://www.blender.org/features/animation/
- Blender manual: https://docs.blender.org/manual/en/latest/animation/index.html
- Unreal animation field guide: https://cdn2.unrealengine.com/animation-field-guide-v1-2-10-b6bd31d52155.pdf
