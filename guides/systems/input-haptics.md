# Input, rebinding and haptics

Reviewed: 2026-08-29

Gameplay code consumes semantic actions (`Jump`, `Confirm`, `Navigate`) rather than physical keys. Keep bindings, device detection, glyph selection and action context outside gameplay rules.

## Input contract

For each action define contexts/action sets, value type, dead zone and curve, press/hold/repeat semantics, buffering, chord/conflict policy, remappability, accessibility alternatives and authoritative/network representation. Preserve keyboard, mouse, touch and controller state independently; last-device UI switching must not discard input.

Rebinding must detect conflicts, allow clearing/reset, support left/right modifiers and unusual controllers, persist per profile and remain operable if a critical action is unbound. Always display glyphs from the current binding rather than hard-coded button art.

Haptics should encode meaning with amplitude, frequency/sharpness, duration, location and envelope. Centralize channels and priorities so overlapping effects cannot saturate continuously. Provide global strength/off and respect system capabilities/preferences; never make haptics the only cue.

Sources:

- Apple Core Haptics: https://developer.apple.com/documentation/corehaptics
- Steam Input: https://partner.steamgames.com/doc/features/steam_controller
- Web Gamepad API: https://developer.mozilla.org/en-US/docs/Games/Techniques/Controls_Gamepad_API
