import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { playReplay, playWithFrameChunks, step, initialState } from "../src/simulation.js";

const replay = JSON.parse(
  await readFile(new URL("../fixtures/golden-replay.json", import.meta.url), "utf8")
);

test("golden replay produces the versioned checkpoints", () => {
  const result = playReplay(replay);
  assert.deepEqual(result.checkpoints, [
    { tick: 4, hash: "53f16f27" },
    { tick: 8, hash: "15324137" },
    { tick: 12, hash: "d282e067" }
  ]);
  assert.equal(result.hash, "d282e067");
});

test("render frame chunking does not alter fixed-tick output", () => {
  const expected = playReplay(replay);
  assert.equal(playWithFrameChunks(replay, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).hash, expected.hash);
  assert.equal(playWithFrameChunks(replay, [3, 1, 4, 2, 2]).hash, expected.hash);
  assert.equal(playWithFrameChunks(replay, [6, 6]).hash, expected.hash);
});

test("non-quantized axis input is rejected", () => {
  assert.throws(
    () => step(initialState(replay.seed), { moveX: 0.5, moveY: 0, collect: false }),
    /quantized integers/
  );
});
