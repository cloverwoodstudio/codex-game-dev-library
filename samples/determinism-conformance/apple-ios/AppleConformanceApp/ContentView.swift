import ConformanceCore
import SpriteKit
import SwiftUI

struct ContentView: View {
    @State private var runID = UUID()

    var body: some View {
        VStack(spacing: 16) {
            SpriteView(scene: makeScene())
                .aspectRatio(16 / 9, contentMode: .fit)
                .clipShape(RoundedRectangle(cornerRadius: 16))
                .overlay(RoundedRectangle(cornerRadius: 16).stroke(.white.opacity(0.15)))
                .accessibilityLabel("Determinism conformance result")

            Button("Replay golden fixture") {
                runID = UUID()
            }
            .buttonStyle(.borderedProminent)
            .accessibilityHint("Runs the deterministic replay again")
        }
        .id(runID)
        .padding()
        .background(Color(red: 0.04, green: 0.06, blue: 0.10).ignoresSafeArea())
    }

    private func makeScene() -> SKScene {
        do {
            guard let url = Bundle.main.url(forResource: "golden-replay", withExtension: "json") else {
                return ConformanceScene.failure("Fixture missing")
            }
            return try ConformanceScene(result: ConformanceSimulation.play(ConformanceSimulation.loadReplay(at: url)))
        } catch {
            return ConformanceScene.failure(String(describing: error))
        }
    }
}
