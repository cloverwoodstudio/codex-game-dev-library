# Character rigging and animation pipeline

Reviewed: 2026-08-29

Animation converts gameplay state into readable intent and physical response. Lock the runtime skeleton, scale, axes, root-motion policy and required animation list before producing volume.

## Rig contract

Define bone hierarchy/names, bind pose, units/axes, root and motion bone, deformation versus control bones, IK/weapon/attachment markers, facial system, maximum influences, twist strategy and LOD bone policy. Export only the deformation skeleton and required markers; control-rig complexity should not leak into runtime unnecessarily.

Skinning acceptance includes extreme-pose silhouette, joint volume, clothing intersections, props, mirrored motion, facial range and target-platform influence/bone limits. Blender's Armature modifier deforms meshes through armatures and vertex groups; preserve a clean source rig separately from engine exports.

## Animation inventory

Organize by gameplay contract: locomotion, traversal, combat/action, reactions, interaction, idle/social, facial/dialogue, cinematic and accessibility variants. For each clip record loop, duration, root motion, contacts, events/notifies, interrupt windows, additive status and source/provenance.

## Runtime graph

Keep authoritative gameplay state separate from visual animation state. Build a small observable state machine or blend graph, with explicit transition priorities and fallbacks. Animation events may request presentation effects; avoid making a fragile visual frame the sole authority for irreversible gameplay unless the timing contract is tested.

## Retargeting

Retargeting reuses motion across proportions or skeletons but requires compatible hierarchy/rig mapping and source/target base poses. Inspect feet, hands, hips, root trajectory, contacts, weapon alignment and silhouette for every body family. Retargeting saves authoring time; it does not eliminate correction passes.

## Test room and budgets

Create an animation gym that exercises every transition at low/high speeds, slopes, turns, interruptions, frame rates and network correction. Track compressed memory, active bone count, graph/update time, skinning cost and simultaneous characters on target hardware.

## Sources

- Blender Armature modifier: https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/armature.html
- Unreal animation retargeting: https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-retargeting-in-unreal-engine
- Unreal animation sequences: https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-sequences-in-unreal-engine
- Godot animation introduction: https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html
