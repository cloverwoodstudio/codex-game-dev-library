# The Codex game-development loop

## 1. Specify

Create `PLAN.md`. Convert taste words into observable acceptance criteria. “Good movement” becomes target speed, acceleration/deceleration, jump height/time, coyote time, input buffering, camera response, and test scenes.

## 2. De-risk

Identify the hardest unknown: networking, procedural generation, target-device performance, animation pipeline, or core feel. Build a disposable spike if necessary.

## 3. Vertical slice

Implement one complete loop with placeholder assets: launch, play, win/fail, restart. Avoid broad content production before this loop is fun and stable.

## 4. Verification ladder

1. Static checks and import validation.
2. Unit tests for deterministic rules.
3. Integration tests for scenes/systems and save/load.
4. Input-driven smoke tests of the real executable.
5. Screenshot/recording review for UI and rendering.
6. Human playtest for feel and comprehension.
7. Profiling on representative target hardware.

## 5. Iterate with evidence

For each meaningful pass, record hypothesis, change, observed result, regression risk, and next action. Keep generated-art prompts in `.prompts/` and concise work logs in `.logs/` when the game repository uses them.

## 6. Content and polish

Only after the loop is sound: expand levels/content, accessibility, localization, audio mix, onboarding, progression, analytics, platform services, and release operations.

## High-value Codex prompts

- “Inspect the repository and write a risk-ranked `PLAN.md`; do not implement yet.”
- “Implement the smallest playable vertical slice and state exact acceptance checks.”
- “Run the game, exercise every control, capture screenshots, and list observed defects before editing.”
- “Add a deterministic reproduction for this bug, then make the smallest fix and rerun it.”
- “Profile on the target configuration; show evidence for the top bottleneck before optimizing.”
