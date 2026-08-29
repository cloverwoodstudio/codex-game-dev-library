import ConformanceCore
import SpriteKit
import UIKit

final class ConformanceScene: SKScene {
    private static let expectedHash = "d282e067"

    init(result: ReplayResult) throws {
        super.init(size: CGSize(width: 960, height: 540))
        scaleMode = .aspectFit
        backgroundColor = UIColor(red: 0.08, green: 0.11, blue: 0.17, alpha: 1)

        let pass = result.hash == Self.expectedHash
        addLabel("iPhone + iPad SpriteKit", x: 42, y: 470, size: 34, color: .white)
        addLabel("Final hash: \(result.hash)", x: 42, y: 414, size: 24, color: .lightGray, monospaced: true)
        addLabel(pass ? "PASS" : "FAIL", x: 42, y: 354, size: 42, color: pass ? .systemGreen : .systemRed)
        addLabel(
            "tick=\(result.state.tick)  score=\(result.state.score)  rng=\(result.state.rngState)",
            x: 42, y: 42, size: 18, color: .systemGray, monospaced: true
        )

        let actor = SKShapeNode(rectOf: CGSize(width: 42, height: 42), cornerRadius: 4)
        actor.fillColor = .systemCyan
        actor.strokeColor = .clear
        actor.position = CGPoint(
            x: 480 + Double(result.state.xMilli) / 100,
            y: 270 - Double(result.state.yMilli) / 100
        )
        addChild(actor)

        guard pass else { throw ConformanceAppError.hashMismatch(result.hash) }
    }

    required init?(coder: NSCoder) { nil }

    static func failure(_ message: String) -> SKScene {
        let scene = SKScene(size: CGSize(width: 960, height: 540))
        scene.scaleMode = .aspectFit
        scene.backgroundColor = .black
        let label = SKLabelNode(text: "FAIL: \(message)")
        label.fontName = "Helvetica Neue"
        label.fontSize = 26
        label.fontColor = .systemRed
        label.position = CGPoint(x: 480, y: 270)
        scene.addChild(label)
        return scene
    }

    private func addLabel(
        _ text: String, x: CGFloat, y: CGFloat, size: CGFloat, color: UIColor, monospaced: Bool = false
    ) {
        let label = SKLabelNode(text: text)
        label.horizontalAlignmentMode = .left
        label.position = CGPoint(x: x, y: y)
        label.fontName = monospaced ? "Menlo" : "Helvetica Neue"
        label.fontSize = size
        label.fontColor = color
        addChild(label)
    }
}

enum ConformanceAppError: Error {
    case hashMismatch(String)
}
