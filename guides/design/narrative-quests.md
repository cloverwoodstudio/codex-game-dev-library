# Interactive narrative, dialogue and quests

Reviewed: 2026-08-29

Narrative state is gameplay state. Model it explicitly, version it, test it and keep presentation separate.

## Narrative design

Begin with player role, dramatic question, themes and agency contract. Track facts the world knows, facts each character knows, relationships, promises, irreversible choices and pending consequences. Prefer branches that reconverge with remembered consequences over exponential content trees without production value.

## Quest model

Use stable IDs and declarative prerequisites. A quest is a graph of conditions, objectives, transitions, outcomes and rewards—not a collection of UI strings. Define cancellation/failure, sequence breaking, duplicate events, reload, multiplayer ownership and content-version behavior.

## Dialogue pipeline

Script → lint/compile → automated traversal → localization extraction → voice/caption association → engine presentation → save-state and controller/navigation QA. Keep dialogue commands typed and allowlisted; text content must not invoke arbitrary engine code.

Tools:

- ink: https://www.inklestudios.com/ink/
- ink writer manual: https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md
- Yarn Spinner: https://www.yarnspinner.dev/docs/

Tool licenses, engine integrations and maturity must be checked for the chosen version.
