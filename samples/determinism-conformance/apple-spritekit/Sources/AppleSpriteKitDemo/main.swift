import AppKit
import ConformanceCore
import SpriteKit

private let expectedHash = "d282e067"

@MainActor
private final class ConformanceScene: SKScene {
    init(result: ReplayResult) {
        super.init(size: CGSize(width: 960, height: 540))
        scaleMode = .aspectFit
        backgroundColor = NSColor(red: 0.08, green: 0.11, blue: 0.17, alpha: 1)

        addLabel("Apple SpriteKit runtime", at: CGPoint(x: 42, y: 470), size: 34, color: .white)
        addLabel("Final hash: \(result.hash)", at: CGPoint(x: 42, y: 414), size: 24, color: .lightGray, monospaced: true)
        let pass = result.hash == expectedHash
        addLabel(pass ? "PASS" : "FAIL", at: CGPoint(x: 42, y: 354), size: 42, color: pass ? .systemGreen : .systemRed)
        addLabel(
            "tick=\(result.state.tick)  score=\(result.state.score)  rng=\(result.state.rngState)",
            at: CGPoint(x: 42, y: 42), size: 18, color: .systemGray, monospaced: true
        )

        let actor = SKShapeNode(rectOf: CGSize(width: 42, height: 42), cornerRadius: 4)
        actor.fillColor = .systemCyan
        actor.strokeColor = .clear
        actor.position = CGPoint(
            x: 480 + Double(result.state.xMilli) / 100,
            y: 270 - Double(result.state.yMilli) / 100
        )
        addChild(actor)
    }

    required init?(coder: NSCoder) { nil }

    private func addLabel(
        _ text: String,
        at position: CGPoint,
        size: CGFloat,
        color: NSColor,
        monospaced: Bool = false
    ) {
        let label = SKLabelNode(text: text)
        label.horizontalAlignmentMode = .left
        label.verticalAlignmentMode = .baseline
        label.position = position
        label.fontName = monospaced ? "Menlo" : "Helvetica Neue"
        label.fontSize = size
        label.fontColor = color
        addChild(label)
    }
}

@MainActor
private func renderSnapshot(result: ReplayResult, to outputURL: URL) throws {
    let view = SKView(frame: CGRect(x: 0, y: 0, width: 960, height: 540))
    let scene = ConformanceScene(result: result)
    view.presentScene(scene)
    view.layoutSubtreeIfNeeded()
    guard let texture = view.texture(from: scene) else {
        throw CocoaError(.fileWriteUnknown)
    }
    let image = texture.cgImage()
    let bitmap = NSBitmapImageRep(cgImage: image)
    guard let png = bitmap.representation(using: .png, properties: [:]) else {
        throw CocoaError(.fileWriteUnknown)
    }
    try png.write(to: outputURL, options: .atomic)
}

let arguments = CommandLine.arguments.dropFirst()
let fixturePath = arguments.first ?? "../fixtures/golden-replay.json"
let snapshotPath = arguments.dropFirst().first ?? "/tmp/apple-spritekit-conformance.png"

do {
    let replay = try ConformanceSimulation.loadReplay(at: URL(fileURLWithPath: fixturePath))
    let result = try ConformanceSimulation.play(replay)
    guard result.hash == expectedHash else {
        fputs("FAIL expected \(expectedHash), got \(result.hash)\n", stderr)
        exit(1)
    }
    try await MainActor.run {
        try renderSnapshot(result: result, to: URL(fileURLWithPath: snapshotPath))
    }
    print("PASS Apple SpriteKit conformance: \(result.hash)")
    print("Snapshot: \(snapshotPath)")
} catch {
    fputs("FAIL \(error)\n", stderr)
    exit(1)
}
