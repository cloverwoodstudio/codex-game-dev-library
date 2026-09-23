# AI Visual Asset Lab
Experimental transport/generation helper for the CW-MECH-001 A/B/C pilot.

Secrets are never committed. Set `TRIPO_API_KEY` only in the local environment/keychain-backed session.
The helper supports read-only balance/status calls and explicit multiview generation through Tripo API v3.
Generation is billable and must only be invoked after owner authorization for the specific run.

Example preflight:
`TRIPO_API_KEY=... python3 tools/ai-visual-asset-lab/tripo_v3.py balance`

Example C generation after source views are approved:
`python3 tools/ai-visual-asset-lab/tripo_v3.py multiview --front ... --left ... --back ... --right ... --texture --pbr`
