extends Node2D

const Simulation = preload("res://src/conformance_simulation.gd")

@onready var actor: Polygon2D = $Actor
@onready var status: Label = $Status


func _ready() -> void:
	var path := ProjectSettings.globalize_path("res://../fixtures/golden-replay.json")
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		status.text = "FAIL: fixture not found"
		return
	var replay: Dictionary = JSON.parse_string(file.get_as_text())
	var result := Simulation.play_replay(replay)
	actor.position = Vector2(480, 300) + Vector2(result.state.xMilli, result.state.yMilli) / 100.0
	status.text = "Final hash: %s\nExpected: d282e067 — %s" % [
		result.hash,
		"PASS" if result.hash == "d282e067" else "FAIL",
	]
