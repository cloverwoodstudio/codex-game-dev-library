# Game audio

Reviewed: 2026-08-29

Design audio as a feedback system: every important player action, danger, success, failure and off-screen event needs an intentional sonic policy.

## Pipeline

Audio brief → source recording/synthesis → edit/clean → variants → metadata/loop points → import/compression → event logic → spatialization → mix/priorities → target-device and accessibility QA.

Use variation sets and controlled pitch/volume randomization to reduce repetition. Set voice limits and priorities. Separate UI, dialogue, SFX, ambience and music buses. Duck by meaning, not merely loudness.

Adaptive music commonly uses horizontal resequencing (changing sections) and vertical layering (adding/removing stems). Drive it with a small, stable set of game parameters and musical transition points.

Sources:

- FMOD learning/integration: https://www.fmod.com/learn
- FMOD concepts: https://www.fmod.com/docs/2.03/studio/fmod-studio-concepts.html
- Wwise interactive music: https://www.audiokinetic.com/en/public-library/2024.1.8_8893/?id=creating_interactive_music&source=Help
