# XR and VR production foundation

Reviewed: 2026-08-29

XR requires physical comfort, stable low-latency rendering, safe spatial interaction and device testing. Simulator/editor success is not release evidence.

## Experience contract

Define supported runtimes/headsets, OpenXR/extensions, play area, seated/standing/room-scale modes, handedness, controllers/hands/gaze, locomotion/turn defaults, recenter, world scale, boundary behavior, passthrough/privacy and sustained frame target.

OpenXR standardizes access across runtimes, but extensions and device capabilities still need discovery and fallback. Never assume hands, controllers, eye tracking, anchors or passthrough are present or permitted.

## Comfort defaults

Default to comfort-friendly locomotion such as teleport and snap turn; let players opt into smooth movement/turning and adjust speed, angle, vignette and direction reference. Avoid unrequested camera motion, roll, acceleration, head bob and loss of tracking reference. Maintain world scale and stable horizon.

Meta recommends minimizing acceleration and optic flow, maintaining consistent frame rate and offering multiple techniques. Provide seated mode, height/reach adjustment, one-handed alternatives and low-fatigue interactions; Apple warns that repeated raised-arm or complex gestures can cause fatigue.

## Interaction

Make targets tolerant, visually and haptically confirm acquisition, prevent accidental activation, and keep important UI within comfortable view/reach. Do not attach large HUD panels rigidly to the head. Handle tracking loss, controller battery/device change and boundary/system overlays gracefully.

## Test matrix

Test every supported device with diverse body sizes, seated/standing, left/right/one hand, glasses where applicable, small play area, tracking loss, recenter, long sessions and comfort options. Measure CPU/GPU frame-time tails, dropped/reprojected frames, motion-to-photon behavior, thermal state and battery.

## Sources

- Khronos OpenXR registry/specification: https://registry.khronos.org/OpenXR/
- Meta locomotion best practices: https://developers.meta.com/horizon/design/locomotion-best-practices/
- Meta locomotion preferences: https://developers.meta.com/horizon/design/locomotion-user-preferences/
- Apple gesture design and comfort: https://developer.apple.com/design/human-interface-guidelines/gestures/
