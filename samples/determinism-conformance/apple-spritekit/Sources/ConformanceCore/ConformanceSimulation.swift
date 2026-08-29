import Foundation

public struct Command: Codable, Sendable {
    public let moveX: Int
    public let moveY: Int
    public let collect: Bool

    public init(moveX: Int, moveY: Int, collect: Bool) {
        self.moveX = moveX
        self.moveY = moveY
        self.collect = collect
    }
}

public struct ReplayFrame: Codable, Sendable {
    public let command: Command
}

public struct Replay: Codable, Sendable {
    public let schemaVersion: Int
    public let algorithmVersion: String
    public let seed: UInt32
    public let tickRate: Int
    public let checkpointEvery: Int
    public let frames: [ReplayFrame]
}

public struct SimulationState: Equatable, Sendable {
    public let version: Int
    public let tick: Int
    public let xMilli: Int
    public let yMilli: Int
    public let score: Int
    public let rngState: UInt32
}

public struct Checkpoint: Equatable, Sendable {
    public let tick: Int
    public let hash: String
}

public struct ReplayResult: Equatable, Sendable {
    public let state: SimulationState
    public let hash: String
    public let checkpoints: [Checkpoint]
}

public enum ConformanceError: Error, Equatable {
    case nonQuantizedAxis
    case incompleteFrameChunks(consumed: Int, expected: Int)
}

public enum ConformanceSimulation {
    private static let hashOffset: UInt32 = 0x811c9dc5
    private static let hashPrime: UInt32 = 0x01000193

    public static func initialState(seed: UInt32) -> SimulationState {
        SimulationState(version: 1, tick: 0, xMilli: 0, yMilli: 0, score: 0, rngState: seed)
    }

    public static func nextU32(_ state: UInt32) -> UInt32 {
        var value: UInt32 = state == 0 ? 0x6d2b79f5 : state
        value ^= value << 13
        value ^= value >> 17
        value ^= value << 5
        return value
    }

    public static func step(_ previous: SimulationState, command: Command) throws -> SimulationState {
        guard (-1000...1000).contains(command.moveX), (-1000...1000).contains(command.moveY) else {
            throw ConformanceError.nonQuantizedAxis
        }
        var rngState = nextU32(previous.rngState)
        let jitter = Int(rngState % 7) - 3
        var collected = 0
        if command.collect {
            rngState = nextU32(rngState)
            if rngState % 5 == 0 { collected = 1 }
        }
        return SimulationState(
            version: 1,
            tick: previous.tick + 1,
            xMilli: previous.xMilli + command.moveX * 17 + jitter,
            yMilli: previous.yMilli + command.moveY * 17 - jitter,
            score: previous.score + collected,
            rngState: rngState
        )
    }

    public static func canonicalState(_ state: SimulationState) -> String {
        [
            "version=\(state.version)",
            "tick=\(state.tick)",
            "xMilli=\(state.xMilli)",
            "yMilli=\(state.yMilli)",
            "score=\(state.score)",
            "rngState=\(state.rngState)"
        ].joined(separator: "\n")
    }

    public static func stateHash(_ state: SimulationState) -> String {
        var hash = hashOffset
        for byte in canonicalState(state).utf8 {
            hash ^= UInt32(byte)
            hash = hash &* hashPrime
        }
        return String(format: "%08x", hash)
    }

    public static func play(_ replay: Replay) throws -> ReplayResult {
        var state = initialState(seed: replay.seed)
        var checkpoints: [Checkpoint] = []
        for frame in replay.frames {
            state = try step(state, command: frame.command)
            if replay.checkpointEvery > 0, state.tick.isMultiple(of: replay.checkpointEvery) {
                checkpoints.append(Checkpoint(tick: state.tick, hash: stateHash(state)))
            }
        }
        return ReplayResult(state: state, hash: stateHash(state), checkpoints: checkpoints)
    }

    public static func play(_ replay: Replay, frameChunks: [Int]) throws -> ReplayResult {
        var state = initialState(seed: replay.seed)
        var commandIndex = 0
        for ticksThisFrame in frameChunks {
            for _ in 0..<ticksThisFrame where commandIndex < replay.frames.count {
                state = try step(state, command: replay.frames[commandIndex].command)
                commandIndex += 1
            }
        }
        guard commandIndex == replay.frames.count else {
            throw ConformanceError.incompleteFrameChunks(consumed: commandIndex, expected: replay.frames.count)
        }
        return ReplayResult(state: state, hash: stateHash(state), checkpoints: [])
    }

    public static func loadReplay(at url: URL) throws -> Replay {
        try JSONDecoder().decode(Replay.self, from: Data(contentsOf: url))
    }
}
