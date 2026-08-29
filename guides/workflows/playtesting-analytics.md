# Playtesting and analytics

Reviewed: 2026-08-29

Playtests answer a question. Separate bug finding, comprehension/usability, balance, appeal and technical scale tests because they need different participants and evidence.

## Session protocol

Define hypothesis and target cohort; freeze build/config; obtain appropriate consent; record build, platform, input and conditions; observe without coaching; collect behavior before opinions; debrief with neutral questions; tag findings by severity/confidence; connect every action item to evidence.

## Minimal event design

Events should answer decisions, not collect everything. Define event name/version, trigger, required properties, units, identity/session semantics, privacy classification, retention and owner. Validate telemetry in development and prevent duplicate/retried events from corrupting counts.

Core diagnostic funnels may include launch → menu → tutorial steps → first loop → fail/win → restart/exit. Add spatial heatmaps only when position and level version are meaningful.

Analytics cannot prove player motivation by itself. Combine event data, performance/crash evidence, session observation, surveys and interviews. Minimize personal data and comply with current platform and regional requirements.

Source: Steam Playtest documentation: https://partner.steamgames.com/doc/features/playtest
