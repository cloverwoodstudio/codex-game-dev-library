# Engine bootstrap

Complete this beside `PLAN.md` before feature scaffolding. Replace every placeholder with a command or decision verified on a clean checkout.

## Toolchain lock

- Engine and exact version:
- Installation source and required modules:
- Language/runtime/compiler versions:
- Package/plugin manifest and lockfile:
- Target platforms and minimum versions:
- Required platform SDKs:
- License or account prerequisites:

## First-run commands

```sh
<install dependencies>
<open or import project>
<run the proof scene>
```

Record required environment variables by name only. Never commit secret values.

## Project boundaries

- Deterministic domain rules live in:
- Engine lifecycle adapters live in:
- Presentation, camera, audio and VFX live in:
- Authored configuration lives in:
- Runtime/save state lives in:
- Tests live in:
- Editable source assets live in:
- Generated/imported/build output ignored by version control:

## Verified commands

| Purpose | Exact command | Expected evidence |
|---|---|---|
| Clean import/compile | `<command>` | zero errors; retained log |
| Focused unit test | `<command>` | successful exit and report |
| Full automated tests | `<command>` | successful exit and report |
| Run proof scene | `<command>` | real controls and transitions exercised |
| Development build | `<command>` | launchable artifact |
| Release-like build | `<command>` | launchable artifact on target |
| Profile | `<command or editor path>` | saved capture and budget comparison |

## Proof scene

Name the smallest scene/map that verifies:

- application boot and clean shutdown;
- input through the real action layer;
- one deterministic state transition;
- pause, restart and return-to-menu behavior where applicable;
- one representative asset from each active pipeline;
- save/load or network authority if those are production-critical;
- development and release-like build launch.

## Initial acceptance checklist

- [ ] A new contributor can install, open and run from these instructions.
- [ ] Exact engine/package versions are locked or deliberately constrained.
- [ ] Generated directories and secrets are excluded from version control.
- [ ] The proof scene works in a real run.
- [ ] Automated checks exit successfully and retain reports.
- [ ] The target build launches outside the editor.
- [ ] Controls and main state transitions were exercised.
- [ ] A representative screenshot or recording was reviewed.
- [ ] Initial performance budgets and a baseline capture exist.
- [ ] Asset licenses and provenance are recorded.
