extends SceneTree

const Simulation = preload("res://src/conformance_simulation.gd")
const EXPECTED_CHECKPOINTS := [
	{"tick": 4, "hash": "53f16f27"},
	{"tick": 8, "hash": "15324137"},
	{"tick": 12, "hash": "d282e067"},
]
const EXPECTED_FINAL_HASH := "d282e067"

var failures := 0


func _init() -> void:
	var fixture_path := ProjectSettings.globalize_path("res://../fixtures/golden-replay.json")
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--fixture="):
			fixture_path = argument.trim_prefix("--fixture=")

	var replay := _load_replay(fixture_path)
	if replay.is_empty():
		quit(1)
		return

	var result := Simulation.play_replay(replay)
	_expect_equal("checkpoint hashes", result.checkpoints, EXPECTED_CHECKPOINTS)
	_expect_equal("final hash", result.hash, EXPECTED_FINAL_HASH)

	for chunks in [
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[3, 1, 4, 2, 2],
		[6, 6],
	]:
		var chunked := Simulation.play_with_frame_chunks(replay, chunks)
		_expect_equal("frame chunks %s" % str(chunks), chunked.hash, EXPECTED_FINAL_HASH)

	var invalid := Simulation.step(
		Simulation.initial_state(int(replay.seed)),
		{"moveX": 0.5, "moveY": 0, "collect": false},
	)
	_expect_equal("non-quantized input rejection", invalid, {})

	if failures == 0:
		print("PASS Godot conformance: %s" % EXPECTED_FINAL_HASH)
	else:
		push_error("FAIL Godot conformance: %d assertion(s)" % failures)
	quit(1 if failures > 0 else 0)


func _load_replay(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Cannot open fixture: %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary:
		push_error("Fixture is not a JSON object: %s" % path)
		return {}
	return parsed


func _expect_equal(label: String, actual: Variant, expected: Variant) -> void:
	if actual != expected:
		failures += 1
		push_error("%s\nexpected: %s\nactual:   %s" % [label, str(expected), str(actual)])
