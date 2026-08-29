import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { initialState, playReplay, playWithFrameChunks, step } from "../src/conformance-simulation.js";

const replay = JSON.parse(await readFile(new URL("../../fixtures/golden-replay.json", import.meta.url), "utf8"));

test("Phaser port matches every golden checkpoint", () => {
  const result = playReplay(replay);
  assert.deepEqual(result.checkpoints, [
    { tick: 4, hash: "53f16f27" },
    { tick: 8, hash: "15324137" },
    { tick: 12, hash: "d282e067" }
  ]);
  assert.equal(result.hash, "d282e067");
});

test("Phaser port is independent of render frame chunks", () => {
  for (const chunks of [[3, 1, 4, 2, 2], [6, 6]]) {
    assert.equal(playWithFrameChunks(replay, chunks).hash, "d282e067");
  }
});

test("Phaser port rejects non-quantized input", () => {
  assert.throws(() => step(initialState(replay.seed), { moveX: 0.5, moveY: 0, collect: false }));
});
