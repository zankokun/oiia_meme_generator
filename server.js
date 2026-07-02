const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const app = express();
const PORT = 3000;

const upload = multer({ dest: 'uploads/' });
const OUTPUT_DIR = path.join(__dirname, 'output');
const FRAMES_DIR = path.join(__dirname, 'frames');

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR, { recursive: true });

app.use(express.static('public'));
app.use('/output', express.static(OUTPUT_DIR));

app.post('/api/generate', upload.single('catPhoto'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No photo uploaded' });

  const inputPath = req.file.path;
  const outputName = `oiia_${Date.now()}.mp4`;
  const outputPath = path.join(OUTPUT_DIR, outputName);

  try {
    await recordVideo(inputPath, outputPath);
    fs.unlinkSync(inputPath);
    res.json({ videoUrl: `/output/${outputName}` });
  } catch (err) {
    console.error('Generation error:', err);
    res.status(500).json({ error: err.message });
  }
});

async function recordVideo(imagePath, outputPath) {
  const puppeteer = require('puppeteer');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--use-gl=angle',
      '--use-angle=gl-egl',
      '--enable-webgl',
      '--ignore-gpu-blocklist',
      '--enable-gpu-rasterization'
    ]
  });

  const page = await browser.newPage();
  page.on('console', msg => console.log(`[scene] ${msg.type()}: ${msg.text()}`));
  page.on('pageerror', err => console.error(`[scene error] ${err.message}`));
  await page.setViewport({ width: 1280, height: 720 });

  const imageData = fs.readFileSync(imagePath).toString('base64');
  const imageUrl = `data:image/jpeg;base64,${imageData}`;

  await page.goto(`http://localhost:${PORT}/scene.html`, { waitUntil: 'networkidle0', timeout: 30000 });

  await page.waitForFunction(() => window.sceneReady === true, { timeout: 10000 });

  await page.evaluate(async (img) => {
    if (window.setCatTexture) await window.setCatTexture(img);
  }, imageUrl);

  const totalFrames = 450;
  const framePaths = [];

  for (let i = 0; i < totalFrames; i++) {
    await page.evaluate((frame) => {
      if (window.renderFrame) window.renderFrame(frame);
    }, i);

    const framePath = path.join(FRAMES_DIR, `frame_${String(i).padStart(4, '0')}.png`);
    const canvas = await page.$('canvas');
    if (canvas) {
      await canvas.screenshot({ path: framePath });
      framePaths.push(framePath);
    }

    if (i % 50 === 0) process.stdout.write(`Frame ${i}/${totalFrames}\r`);
  }

  console.log(`\nAll ${totalFrames} frames captured`);

  await browser.close();

  const audioPath = path.join(__dirname, 'assets', 'music', 'OIIA.mp3');
  const tempVideo = outputPath.replace('.mp4', '_noaudio.mp4');

  let ffmpegEncoder;
  try {
    execSync('ffmpeg -hide_banner -encoders 2>&1 | findstr h264_nvenc', { stdio: 'pipe' });
    ffmpegEncoder = 'h264_nvenc';
    console.log('Using GPU encoding (NVENC)');
  } catch {
    ffmpegEncoder = 'libx264';
    console.log('Using CPU encoding (libx264)');
  }

  const encArgs = ffmpegEncoder === 'h264_nvenc'
    ? `-c:v h264_nvenc -preset p4 -cq 23`
    : `-c:v libx264 -preset fast -crf 23`;

  execSync(`ffmpeg -y -framerate 30 -i "${path.join(FRAMES_DIR, 'frame_%04d.png')}" ${encArgs} -pix_fmt yuv420p -vf "scale=1280:720" "${tempVideo}"`, { stdio: 'inherit' });

  if (fs.existsSync(audioPath)) {
    execSync(`ffmpeg -y -i "${tempVideo}" -i "${audioPath}" -c:v copy -c:a aac -b:a 128k -shortest "${outputPath}"`, { stdio: 'inherit' });
    fs.unlinkSync(tempVideo);
  } else {
    fs.renameSync(tempVideo, outputPath);
  }

  framePaths.forEach(f => { if (fs.existsSync(f)) fs.unlinkSync(f); });

  console.log(`Video saved: ${outputPath}`);
}

app.listen(PORT, () => {
  console.log(`OIIA Cat Meme Generator: http://localhost:${PORT}`);
});
