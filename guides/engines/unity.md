# Unity production playbook

Reviewed: 2026-08-29

## Best fit

Choose Unity for broad platform reach, a large C# ecosystem, mature integrations, and teams that benefit from its component workflow. Lock the exact editor version and verify packages, render pipeline, platform modules and licensing assumptions before scaffolding.

## Recommended project shape

```text
Assets/Game/
  Core/          # pure C# rules and shared contracts
  Features/      # vertical features with assembly definitions
  Presentation/  # views, animation, audio, effects and UI
  Content/       # authored data, scenes and prefabs
  Tests/         # EditMode and PlayMode assemblies
  Editor/        # build and authoring tools only
Packages/manifest.json
ProjectSettings/
```

- Use assembly definitions to make dependencies explicit and control compile/test scope.
- Put deterministic rules in plain C# where possible; use `MonoBehaviour` as an engine adapter, not the home of every rule.
- Treat ScriptableObjects primarily as authored configuration. Keep runtime and save state in explicit models unless shared asset mutation is intentional.
- Preserve `.meta` files. Never edit or commit generated `Library/`, `Temp/`, `Logs/` or build output.
- Configure Unity Smart Merge or an equivalent reviewed process for text-serialized scenes and prefabs. It reduces conflicts but cannot make semantic merges automatically safe.

## Codex loop

1. Read `ProjectVersion.txt`, `Packages/manifest.json`, relevant assembly definitions, scenes/prefabs and owning scripts.
2. Add or update a focused Edit Mode test for pure logic.
3. Implement through the smallest feature boundary; avoid unrelated scene serialization churn.
4. Run focused tests, then Play Mode validation for engine behavior.
5. Open the scene, exercise controls and transitions, and inspect Game view evidence.
6. Build and launch the intended player; Editor play mode is not release proof.

Typical command shapes vary by Unity version and installed path. Put exact working commands in the project bootstrap document:

```sh
Unity -batchmode -projectPath <project> -runTests -testPlatform EditMode -testResults <results.xml>
Unity -batchmode -projectPath <project> -runTests -testPlatform PlayMode -testResults <results.xml>
Unity -batchmode -quit -projectPath <project> -activeBuildProfile <profile> -build <output>
```

Unity build options evolve across releases. Pin documentation to the project's editor version and prefer a version-controlled build method when custom scenes, settings, signing or multiple targets are involved.

## Validation ladder

1. Edit Mode tests for pure C# rules.
2. Asset import and script compilation on a clean checkout.
3. Play Mode tests for component and scene behavior.
4. Manual controls and state-transition pass in a representative scene.
5. Development player smoke test with logs retained.
6. Release-like IL2CPP/AOT build on the target device.
7. Unity Profiler capture from the target player.

## Build and asset traps

- Test IL2CPP/AOT, managed stripping, reflection and serialization early; Editor/Mono success is insufficient.
- Keep addressable or streamed content ownership explicit and test missing, stale and slow downloads.
- Audit shader variants and render-pipeline settings on actual target GPUs.
- Avoid relying on scene object names, list order or editor-only APIs as stable identifiers.
- Commit package manifests and supported lockfiles; isolate package upgrades as reviewable changes.

## Performance rules

Define CPU, GPU, memory, loading, draw-call, physics and garbage-collection budgets per target. Profile builds on target hardware. Deep Profile is diagnostic instrumentation with substantial overhead, not a representative shipping baseline.

## Primary sources

- [Build from the command line](https://docs.unity3d.com/6000.0/Documentation/Manual/build-command-line.html)
- [Unity Test Framework command line](https://docs.unity3d.com/Packages/com.unity.test-framework@2.0/manual/reference-command-line.html)
- [Unity Profiler](https://docs.unity3d.com/Manual/Profiler.html)
- [Unity Smart Merge](https://docs.unity.cn/Manual/SmartMerge.html)
