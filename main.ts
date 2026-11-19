// main.ts — entry point for the make.fun run.
// The front page is drawn ahead of time by generate.py and stored as
// entry.png next to this file. All this program does is place a copy
// of that image at <output>/entry.png, so the run is deterministic:
// the same bytes come out every time, in any output directory.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
