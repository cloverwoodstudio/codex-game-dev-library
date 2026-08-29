# Browser games

Reviewed: 2026-08-29

OpenAI's official browser-game workflow recommends a written plan, an `AGENTS.md`, live browser testing, reusable ImageGen prompts, and current framework docs. Its practical default is Next.js with Phaser or PixiJS; persistence-heavy games may add Fastify, WebSockets, Postgres, and Redis.

Use Phaser for conventional 2D game structure; PixiJS when you mainly need a renderer; Three.js/Babylon.js for 3D. Keep simulation separate from rendering, expose debug state, seed randomness, and provide stable test hooks. Do not rely only on DOM tests: canvas output requires screenshots and actual input playback.

Browser checklist: keyboard/pointer/touch/gamepad, focus loss, pause/resume, audio unlock, resize/orientation, device-pixel ratio, mobile thermal limits, asset caching, offline/slow network, accessibility outside and inside canvas, and cross-browser behavior.

Primary source: https://learn.chatgpt.com/use-cases/browser-games
