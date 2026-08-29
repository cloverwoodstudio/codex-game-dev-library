import Foundation
import Testing
@testable import ConformanceCore

private let expectedCheckpoints = [
    Checkpoint(tick: 4, hash: "53f16f27"),
    Checkpoint(tick: 8, hash: "15324137"),
    Checkpoint(tick: 12, hash: "d282e067")
]

private func fixture() throws -> Replay {
    let packageDirectory = URL(fileURLWithPath: #filePath)
        .deletingLastPathComponent()
        .deletingLastPathComponent()
        .deletingLastPathComponent()
    return try ConformanceSimulation.loadReplay(
        at: packageDirectory.appending(path: "../fixtures/golden-replay.json").standardizedFileURL
    )
}

@Test("Swift port matches golden replay")
func goldenReplay() throws {
    let result = try ConformanceSimulation.play(fixture())
    #expect(result.checkpoints == expectedCheckpoints)
    #expect(result.hash == "d282e067")
}

@Test("Swift port ignores render frame chunking", arguments: [[3, 1, 4, 2, 2], [6, 6]])
func frameChunks(_ chunks: [Int]) throws {
    #expect(try ConformanceSimulation.play(fixture(), frameChunks: chunks).hash == "d282e067")
}

@Test("Swift port rejects out-of-contract input")
func rejectsInvalidInput() {
    #expect(throws: ConformanceError.nonQuantizedAxis) {
        try ConformanceSimulation.step(
            ConformanceSimulation.initialState(seed: 1),
            command: Command(moveX: 1001, moveY: 0, collect: false)
        )
    }
}
