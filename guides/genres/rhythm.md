# Rhythm game playbook

Reviewed: 2026-08-29

## Product loop

Anticipate musical event → act against an audio clock → receive precise timing feedback → maintain phrase/combo → recover → complete song/performance.

## Smallest vertical slice

One licensed/original track, versioned beat map, one input action, at least three timing judgments, calibration, pause/restart, results screen, input/audio/visual offset settings and deterministic scoring replay.

## High-risk contracts

- audio hardware clock as timing authority, not render frames;
- device-specific output/input/display latency calibration;
- beat map time base, tempo/time-signature changes and versioning;
- input timestamping before presentation delay;
- fair timing windows, score/combo order and dropped-frame behavior;
- photosensitivity, motion, captions and non-color-only cues.

## Timing lab

Inject synthetic inputs at known offsets across frame rates, audio buffers and devices. Verify judgment boundaries, pause/resume/seek, long-song drift and controller polling. Preserve raw offset histograms rather than only final scores.

## Typical traps

Using animation position as clock, ignoring Bluetooth/TV latency, accumulating float drift, beat-map edits invalidating scores, calibration with ambiguous cues, copyrighted music without synchronization/use rights and effects obscuring timing targets.

## References

- Godot gameplay/audio synchronization: https://docs.godotengine.org/en/stable/tutorials/audio/sync_with_audio.html
- Library adaptive-audio guide: ../systems/adaptive-audio.md
- Xbox photosensitivity guideline: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/118
