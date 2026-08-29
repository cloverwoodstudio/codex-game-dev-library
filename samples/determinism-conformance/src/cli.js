import { readFile } from "node:fs/promises";
import { playReplay } from "./simulation.js";

const replayPath = process.argv[2];
if (!replayPath) throw new Error("Usage: node src/cli.js <replay.json>");

const replay = JSON.parse(await readFile(replayPath, "utf8"));
const result = playReplay(replay);
process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
