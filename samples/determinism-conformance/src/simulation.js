const HASH_OFFSET = 0x811c9dc5;
const HASH_PRIME = 0x01000193;

export class XorShift32 {
  constructor(seed) {
    this.state = seed >>> 0;
    if (this.state === 0) this.state = 0x6d2b79f5;
  }

  nextU32() {
    let value = this.state;
    value ^= value << 13;
    value ^= value >>> 17;
    value ^= value << 5;
    this.state = value >>> 0;
    return this.state;
  }
}

export function initialState(seed) {
  return {
    version: 1,
    tick: 0,
    xMilli: 0,
    yMilli: 0,
    score: 0,
    rngState: seed >>> 0
  };
}

export function step(previous, command) {
  const rng = new XorShift32(previous.rngState);
  const jitter = Number(rng.nextU32() % 7) - 3;
  const dx = clampAxis(command.moveX) * 17;
  const dy = clampAxis(command.moveY) * 17;
  const collected = command.collect && rng.nextU32() % 5 === 0 ? 1 : 0;

  return {
    version: 1,
    tick: previous.tick + 1,
    xMilli: previous.xMilli + dx + jitter,
    yMilli: previous.yMilli + dy - jitter,
    score: previous.score + collected,
    rngState: rng.state
  };
}

export function canonicalState(state) {
  return [
    `version=${state.version}`,
    `tick=${state.tick}`,
    `xMilli=${state.xMilli}`,
    `yMilli=${state.yMilli}`,
    `score=${state.score}`,
    `rngState=${state.rngState}`
  ].join("\n");
}

export function fnv1a32(text) {
  let hash = HASH_OFFSET;
  for (const byte of new TextEncoder().encode(text)) {
    hash ^= byte;
    hash = Math.imul(hash, HASH_PRIME) >>> 0;
  }
  return hash.toString(16).padStart(8, "0");
}

export function stateHash(state) {
  return fnv1a32(canonicalState(state));
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

export function playWithFrameChunks(replay, frameChunks) {
  let state = initialState(replay.seed);
  let commandIndex = 0;
  for (const ticksThisFrame of frameChunks) {
    for (let tick = 0; tick < ticksThisFrame && commandIndex < replay.frames.length; tick += 1) {
      state = step(state, replay.frames[commandIndex].command);
      commandIndex += 1;
    }
  }
  if (commandIndex !== replay.frames.length) {
    throw new Error(`Frame chunks consumed ${commandIndex}/${replay.frames.length} ticks`);
  }
  return { state, hash: stateHash(state) };
}

function clampAxis(value) {
  if (!Number.isInteger(value)) throw new TypeError("Axis values must be quantized integers");
  return Math.max(-1000, Math.min(1000, value));
}
