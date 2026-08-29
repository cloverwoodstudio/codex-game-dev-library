const U32_MASK = 0xffffffff;
const HASH_OFFSET = 0x811c9dc5;
const HASH_PRIME = 0x01000193;

export function initialState(seed) {
  return { version: 1, tick: 0, xMilli: 0, yMilli: 0, score: 0, rngState: seed >>> 0 };
}

export function nextU32(state) {
  let value = state >>> 0;
  if (value === 0) value = 0x6d2b79f5;
  value ^= value << 13;
  value ^= value >>> 17;
  value ^= value << 5;
  return value >>> 0;
}

export function step(previous, command) {
  const moveX = quantizedAxis(command.moveX);
  const moveY = quantizedAxis(command.moveY);
  let rngState = nextU32(previous.rngState);
  const jitter = (rngState % 7) - 3;
  let collected = 0;
  if (command.collect) {
    rngState = nextU32(rngState);
    if (rngState % 5 === 0) collected = 1;
  }
  return {
    version: 1,
    tick: previous.tick + 1,
    xMilli: previous.xMilli + moveX * 17 + jitter,
    yMilli: previous.yMilli + moveY * 17 - jitter,
    score: previous.score + collected,
    rngState
  };
}

export function canonicalState(state) {
  return ["version", "tick", "xMilli", "yMilli", "score", "rngState"]
    .map((field) => `${field}=${state[field]}`)
    .join("\n");
}

export function stateHash(state) {
  let hash = HASH_OFFSET;
  for (const byte of new TextEncoder().encode(canonicalState(state))) {
    hash ^= byte;
    hash = Math.imul(hash, HASH_PRIME) & U32_MASK;
  }
  return (hash >>> 0).toString(16).padStart(8, "0");
}

export function playReplay(replay) {
  let state = initialState(replay.seed);
  const checkpoints = [];
  for (const frame of replay.frames) {
    state = step(state, frame.command);
    if (replay.checkpointEvery > 0 && state.tick % replay.checkpointEvery === 0) {
      checkpoints.push({ tick: state.tick, hash: stateHash(state) });
    }
  }
  return { state, hash: stateHash(state), checkpoints };
}

export function playWithFrameChunks(replay, chunks) {
  let state = initialState(replay.seed);
  let commandIndex = 0;
  for (const ticksThisFrame of chunks) {
    for (let tick = 0; tick < ticksThisFrame && commandIndex < replay.frames.length; tick += 1) {
      state = step(state, replay.frames[commandIndex].command);
      commandIndex += 1;
    }
  }
  if (commandIndex !== replay.frames.length) throw new Error("Frame chunks did not consume replay");
  return { state, hash: stateHash(state) };
}

function quantizedAxis(value) {
  if (!Number.isInteger(value)) throw new TypeError("Axis values must be quantized integers");
  return Math.max(-1000, Math.min(1000, value));
}
