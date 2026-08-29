# In-game cinematics and scripted sequences

Reviewed: 2026-08-29

Cinematics must enter and leave gameplay safely. Treat each sequence as a versioned state transition with camera, input, audio, subtitle, save and skip contracts—not merely a timeline.

## Sequence contract

Record trigger/preconditions, bound actors, start/end state, camera ownership, input policy, skippability, checkpoint/save behavior, dialogue/subtitle IDs, localization timing, gameplay events, multiplayer authority and failure recovery.

Separate shots/subsequences so collaborators can work independently and reuse material. Unreal Sequencer stores tracks, cameras, keyframes and animations in Level Sequence assets bound through Level Sequence Actors; Unity Timeline similarly supports cinematic, gameplay, audio and particle sequences.

## Safe playback

- Validate all required actors/assets before taking control.
- Save or checkpoint before a high-risk transition.
- Define what happens on pause, skip, death, disconnect, unload and replay.
- Make skip jump to one idempotent end-state function; do not fast-forward every side effect blindly.
- Restore camera, input, HUD, time scale and audio mix explicitly.
- Server-authoritative multiplayer decides shared state; clients may present local cameras.

## Accessibility and localization

Provide subtitles/captions, speaker identity, readable timing and safe areas. Avoid encoding required information solely in camera motion, audio or rapid cuts. Offer motion-reduction alternatives where cinematic movement is intense. Recheck timing for localized dialogue and expanded text.

## Test matrix

Test first play, replay, immediate/mid/late skip, pause/resume, save/load boundary, missing optional actor, low frame rate, different aspect ratios/locales, subtitles, reduced motion and multiplayer join/leave where applicable. Verify the exact post-sequence gameplay state.

## Sources

- Unreal Sequencer overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-sequencer-movie-tool-overview
- Unreal sequences, shots and takes: https://dev.epicgames.com/documentation/en-us/unreal-engine/sequences-shots-and-takes-in-unreal-engine
- Unity Timeline: https://docs.unity3d.com/Manual/com.unity.timeline.html
