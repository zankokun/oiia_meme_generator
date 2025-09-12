# Copilot Instructions for `oiia_meme_generator`

## Overview
This project generates a meme video featuring a cat with the OIIA soundtrack. It combines image background removal, animation, and audio overlay using Python and several external libraries.

## Architecture & Workflow
- **Main script:** `generate_oiia_cat_meme.py` orchestrates the workflow.
- **Inputs:**
  - `stand.png` — image of a standing cat
  - `sit.png` — image of a sitting cat
  - `OIIA.mp3` — optional audio file
- **Processing:**
  - Backgrounds are removed from cat images using `rembg`.
  - Images are resized and animated (rotation, scaling, mirroring) with OpenCV and numpy.
  - Frames are composed with a green background.
  - Video is generated using `moviepy` and optionally synchronized with audio.
- **Output:**
  - `oiia_cat_meme.mp4` — final meme video

## Key Patterns & Conventions
- **Image Handling:** Always ensure input images have an alpha channel after background removal. The script expects RGBA images.
- **Animation:** The sitting cat is animated with a simulated 3D rotation (width scaling and mirroring) for 3 seconds; the standing cat is shown statically for 2 seconds.
- **Frame Composition:** All frames are centered and composited over a solid green background (`BG_COLOR`).
- **Audio Integration:** If `OIIA.mp3` exists, it is clipped to 5 seconds and added to the video.
- **Error Handling:** The script prints clear error messages if required files are missing or images lack an alpha channel.

## Developer Workflow
- **Dependencies:**
  - Install Python packages from `requirements.txt`.
  - Install system dependency for OpenCV: `sudo apt update && sudo apt install -y libgl1`
- **Run:**
  - Execute `python generate_oiia_cat_meme.py` to generate the meme video.
- **Debugging:**
  - Check for missing files or incorrect image formats if errors occur.
  - The script prints progress and error messages to the console.

## External Libraries
- `opencv-python` (cv2)
- `rembg` (background removal)
- `moviepy` (video/audio composition)
- `Pillow` (image format conversion)
- `numpy`

## Example Usage
```bash
sudo apt update && sudo apt install -y libgl1
pip install -r requirements.txt
python generate_oiia_cat_meme.py
```

## File Reference
- `generate_oiia_cat_meme.py`: Main logic and workflow
- `stand.png`, `sit.png`: Cat images
- `OIIA.mp3`: Audio file
- `oiia_cat_meme.mp4`: Output video

---
For questions or improvements, review the script and README for current conventions. If you add new features, document any new patterns here.
