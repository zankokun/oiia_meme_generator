# OIIA Cat Meme Generator - Agent Instructions

## Project Overview
Upload a cat photo → get a ~15s spinning meme video with music.

## Architecture

```
Cat Photo
  ↓
[1] Express Server — handles upload
  ↓
[2] Puppeteer — opens three.js scene
  ↓
[3] Three.js — procedural cat model + user texture
  ↓
[4] Frame Capture — 450 PNG frames (15s × 30fps)
  ↓
[5] FFmpeg — frames → MP4 + audio
  ↓
Final MP4
```

## Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| Server | Express + Multer | Simple file upload |
| 3D Rendering | Three.js (r170) | Browser-based WebGL, procedural cat |
| Frame Capture | Puppeteer | Headless Chrome screenshots |
| Video Encoding | FFmpeg | Standard, reliable |
| Frontend | Vanilla HTML/JS | No framework needed |

## Key Design Decisions

1. **Procedural cat model**: Built from primitives (spheres, cones, cylinders) in three.js — no external 3D model files needed.
2. **User texture overlay**: User's cat photo is applied as texture to the procedural model.
3. **Puppeteer for recording**: Headless Chrome renders WebGL frames, captures screenshots.
4. **FFmpeg for final video**: Concat frames into MP4 with audio overlay.

## Constraints

- Requires FFmpeg installed on system
- Requires Node.js 18+
- Generation time: ~2-5 min for 15s video (450 frames)
- Output: 720p MP4, 15 seconds, 30fps

## Commands

```bash
npm install
npm start          # Web UI on port 3000
```

## File Structure
```
oiia/
├── AGENTS.md
├── README.md
├── package.json
├── server.js           # Express server + recording logic
├── public/
│   ├── index.html      # Upload UI
│   └── scene.html      # Three.js 3D scene
├── models/             # (empty, procedural cat)
├── assets/music/
│   └── OIIA.mp3
├── output/             # Generated videos
└── frames/             # Temp frame storage
```
