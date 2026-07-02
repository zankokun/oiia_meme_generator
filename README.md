# OIIA Cat Meme Generator

Upload a cat photo → get a spinning 3D meme video with music.

## How It Works

1. Upload your cat photo
2. Three.js procedural cat model is textured with your photo
3. 450 frames are captured (15s × 30fps)
4. FFmpeg combines frames + OIIA music into MP4

## Requirements

- Node.js 18+
- FFmpeg installed and in PATH

## Setup

```bash
npm install
npm start
```

Open http://localhost:3000

## Tech Stack

- **Three.js** — 3D procedural cat model
- **Puppeteer** — frame capture from WebGL
- **FFmpeg** — video encoding
- **Express** — web server
