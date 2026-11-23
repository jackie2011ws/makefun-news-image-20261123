// Sum up 23 November's world news in one image — graded entry program.
// Node 22, standard library only. The image is stored as base64 text in
// entry.png.b64 in this repository (GitHub text push cannot carry the raw
// PNG); this program decodes it to the output directory as entry.png,
// unchanged, so two runs always write the same bytes (no network, no clock,
// no random). Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// In the grader, MAKEFUN_OUTPUT_DIR is not set, so it writes to /output.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const b64 = readFileSync(new URL("./entry.png.b64", import.meta.url), "utf8").replace(/\s/g, "");
writeFileSync(join(outDir, "entry.png"), Buffer.from(b64, "base64"));
