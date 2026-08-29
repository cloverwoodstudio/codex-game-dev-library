# Unity

Reviewed: 2026-08-29

Use assembly definitions and feature-oriented boundaries to control compile/test scope. Keep pure C# rules outside `MonoBehaviour` where possible. Separate authored data, runtime state, and presentation. Use Edit Mode tests for pure logic and Play Mode tests for engine behavior; validate actual builds, not only Editor play mode.

Profile before optimizing and measure on target hardware. Treat deep profiling as diagnostic instrumentation with meaningful overhead.

Primary sources:

- https://docs.unity3d.com/Manual/com.unity.test-framework.html
- https://docs.unity3d.com/Manual/Profiler.html
- https://docs.unity3d.com/Manual/BestPracticeUnderstandingPerformanceInUnity.html
