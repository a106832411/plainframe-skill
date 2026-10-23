/**
 * 逐句配音：读取 lines.json，为每句生成 mp3 + 24k 单声道 wav
 * 用法：node gen_tts.mjs <音频目录>
 * 依赖：npm i msedge-tts
 */
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { MsEdgeTTS, OUTPUT_FORMAT } from "msedge-tts";

const cfg = JSON.parse(fs.readFileSync(new URL("./lines.json", import.meta.url), "utf8"));
const outRoot = process.argv[2] || "./_tts";
fs.mkdirSync(outRoot, { recursive: true });

for (const line of cfg.lines) {
  const dir = path.join(outRoot, "e" + String(line.n).padStart(2, "0"));
  fs.mkdirSync(dir, { recursive: true });

  const tts = new MsEdgeTTS({ connectionTimeoutMs: 20000, synthesisTimeoutMs: 90000 });
  await tts.setMetadata(cfg.voice, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3);
  await tts.toFile(dir, line.text, { rate: cfg.rate, pitch: cfg.pitch });

  // 转 24k 单声道 wav
  execFileSync("ffmpeg", ["-y", "-loglevel", "error",
    "-i", path.join(dir, "audio.mp3"),
    "-ar", "24000", "-ac", "1", path.join(dir, "audio.wav")], { stdio: "ignore" });

  console.log("ok", line.n, line.text);
}
console.log("done →", outRoot);
process.exit(0);
