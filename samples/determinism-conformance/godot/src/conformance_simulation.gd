class_name ConformanceSimulation
extends RefCounted

const U32_MASK := 0xffffffff
const HASH_OFFSET := 0x811c9dc5
const HASH_PRIME := 0x01000193


static func initial_state(seed: int) -> Dictionary:
	return {
		"version": 1,
		"tick": 0,
		"xMilli": 0,
		"yMilli": 0,
		"score": 0,
		"rngState": seed & U32_MASK,
	}


static func next_u32(state: int) -> int:
	var value := state & U32_MASK
	if value == 0:
		value = 0x6d2b79f5
	value = (value ^ ((value << 13) & U32_MASK)) & U32_MASK
	value = (value ^ (value >> 17)) & U32_MASK
	value = (value ^ ((value << 5) & U32_MASK)) & U32_MASK
	return value


static func step(previous: Dictionary, command: Dictionary) -> Dictionary:
	if not _is_quantized_axis(command.get("moveX")) or not _is_quantized_axis(command.get("moveY")):
		return {}
	var move_x := _quantized_axis(command.get("moveX"))
	var move_y := _quantized_axis(command.get("moveY"))
	var rng_state := next_u32(int(previous.rngState))
	var jitter := (rng_state % 7) - 3
	var collected := 0
	if bool(command.get("collect", false)):
		rng_state = next_u32(rng_state)
		if rng_state % 5 == 0:
			collected = 1

	return {
		"version": 1,
		"tick": int(previous.tick) + 1,
		"xMilli": int(previous.xMilli) + move_x * 17 + jitter,
		"yMilli": int(previous.yMilli) + move_y * 17 - jitter,
		"score": int(previous.score) + collected,
		"rngState": rng_state,
	}


static func canonical_state(state: Dictionary) -> String:
	return "\n".join([
		"version=%d" % int(state.version),
		"tick=%d" % int(state.tick),
		"xMilli=%d" % int(state.xMilli),
		"yMilli=%d" % int(state.yMilli),
		"score=%d" % int(state.score),
		"rngState=%d" % int(state.rngState),
	])


static func fnv1a32(text: String) -> String:
	var hash_value := HASH_OFFSET
	for byte in text.to_utf8_buffer():
		hash_value = hash_value ^ int(byte)
		hash_value = (hash_value * HASH_PRIME) & U32_MASK
	return "%08x" % hash_value


static func state_hash(state: Dictionary) -> String:
	return fnv1a32(canonical_state(state))


static func play_replay(replay: Dictionary) -> Dictionary:
	var state := initial_state(int(replay.seed))
	var checkpoints: Array[Dictionary] = []
	var checkpoint_every := int(replay.get("checkpointEvery", 0))
	for frame in replay.frames:
		state = step(state, frame.command)
		if checkpoint_every > 0 and int(state.tick) % checkpoint_every == 0:
			checkpoints.append({"tick": state.tick, "hash": state_hash(state)})
	return {"state": state, "hash": state_hash(state), "checkpoints": checkpoints}


static func play_with_frame_chunks(replay: Dictionary, frame_chunks: Array) -> Dictionary:
	var state := initial_state(int(replay.seed))
	var command_index := 0
	for ticks_this_frame in frame_chunks:
		for unused_tick in range(ticks_this_frame):
			if command_index >= replay.frames.size():
				break
			state = step(state, replay.frames[command_index].command)
			command_index += 1
	if command_index != replay.frames.size():
		push_error("Frame chunks consumed %d/%d ticks" % [command_index, replay.frames.size()])
		return {}
	return {"state": state, "hash": state_hash(state)}


static func _quantized_axis(value: Variant) -> int:
	return clampi(int(value), -1000, 1000)


static func _is_quantized_axis(value: Variant) -> bool:
	return value is int or (value is float and value == floor(value))
