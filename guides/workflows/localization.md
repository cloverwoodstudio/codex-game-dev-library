# Internationalization, localization and voice

Reviewed: 2026-08-29

Internationalize from the first UI and narrative systems even if translation starts later. Source text embedded as layout is technical debt.

## Data contract

Every player-facing string has a stable ID, source text, developer context, speaker, character limit where real, placeholders with types, plural/select rules, rich-text constraints, screenshot reference, status and content version. Never concatenate translated sentence fragments.

## Pipeline

Extract/gather → validate IDs/placeholders → pseudo-localize → export standard exchange format → translate/review → import → automated completeness checks → linguistic QA in context → platform/store metadata → regression pass.

Test expansion, very short strings, accented text, CJK line breaking, complex scripts, right-to-left layout, mixed-direction numbers/names, font fallback, input glyphs, subtitles, controller navigation and runtime locale changes. Pseudo-localization belongs in CI.

Voice assets need stable line IDs, final script/context, pronunciation notes, casting/consent records, take/version mapping, loudness/noise QA, localized timing strategy and matching captions. Never use synthetic or cloned voices without documented rights and consent.

Sources:

- Unity Localization: https://docs.unity3d.com/Packages/com.unity.localization@1.0/manual/index.html
- Unreal localization tools: https://dev.epicgames.com/documentation/en-us/unreal-engine/localization-tools-in-unreal-engine
- Godot internationalization: https://docs.godotengine.org/en/stable/tutorials/i18n/index.html
- W3C internationalization tests: https://www.w3.org/International/i18n-tests/
