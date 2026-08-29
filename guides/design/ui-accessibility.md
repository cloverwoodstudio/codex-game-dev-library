# Game UI, UX and accessibility

Reviewed: 2026-08-29

Design accessibility with the core interaction, not as a final settings screen. Important information should not rely on color, sound, text, motion or haptics alone.

## UI states

Every interactive element needs visible default, hover, focus, pressed, disabled, loading, success and error behavior where applicable. Navigation must work with every supported input, preserve focus sensibly and never trap the player.

## Baseline

- rebindable controls and alternatives to holds, rapid presses and simultaneous inputs
- scalable readable text, safe-area handling and complete localized glyph coverage
- subtitles/captions with speaker identification and configurable presentation
- redundant cues across visual/audio/haptic channels
- color-independent state and tested contrast
- motion reduction, camera shake, blur and flashing controls
- separate difficulty dimensions where possible; do not tie accessibility to punishment
- pause/time-limit assistance where the design permits
- screen narration/semantic UI strategy when platform and genre support it

Test from first launch through gameplay, pause, failure, recovery and exit. Settings must be accessible before the first unskippable interaction.

Sources:

- Xbox Accessibility Guidelines: https://learn.microsoft.com/en-us/xbox/accessibility/guidelines
- Game Accessibility Guidelines: https://gameaccessibilityguidelines.com/
