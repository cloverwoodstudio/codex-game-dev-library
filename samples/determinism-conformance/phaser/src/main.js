import Phaser from "phaser";
import replay from "../../fixtures/golden-replay.json";
import { playReplay } from "./conformance-simulation.js";

const EXPECTED_HASH = "d282e067";

class ConformanceScene extends Phaser.Scene {
  constructor() {
    super("ConformanceScene");
  }

  create() {
    const result = playReplay(replay);
    const pass = result.hash === EXPECTED_HASH;
    this.cameras.main.setBackgroundColor(0x20283a);
    this.add.text(36, 34, "Phaser 4 runtime", { fontFamily: "system-ui", fontSize: 34, color: "#eef4ff" });
    this.add.text(36, 92, `Final hash: ${result.hash}`, { fontFamily: "monospace", fontSize: 24, color: "#c8d7f2" });
    this.add.text(36, 132, pass ? "PASS" : "FAIL", { fontFamily: "system-ui", fontSize: 40, color: pass ? "#62e6a7" : "#ff6b7a" });
    this.add.rectangle(480 + result.state.xMilli / 100, 310 + result.state.yMilli / 100, 42, 42, 0x39bdf8);
    this.add.text(36, 482, `tick=${result.state.tick}  score=${result.state.score}  rng=${result.state.rngState}`, {
      fontFamily: "monospace", fontSize: 18, color: "#91a4c7"
    });
    document.documentElement.dataset.conformance = pass ? "pass" : "fail";
    window.__CONFORMANCE__ = { ...result, pass };
  }
}

new Phaser.Game({
  type: Phaser.AUTO,
  width: 960,
  height: 540,
  parent: "game",
  backgroundColor: "#20283a",
  scene: [ConformanceScene],
  render: { antialias: true, pixelArt: false }
});
