import cv2
import numpy as np
from rembg import remove
from moviepy import ImageSequenceClip, AudioFileClip
import os

# --- Конфигурация ---
STAND_IMG = 'stand.png'  # Картинка стоящего кота
SIT_IMG = 'sit.png'      # Картинка сидящего кота
AUDIO_FILE = 'music.mp3' # Музыка (опционально)
OUTPUT_VIDEO = 'oiia_cat_meme.mp4'
FPS = 30
DURATION = 10  # секунд
BG_COLOR = (0, 255, 0)  # Зеленый фон

# --- Вспомогательные функции ---
def extract_cat(img_path):
    img = cv2.imread(img_path)
    img_rgba = remove(img)
    return img_rgba


def create_frames(cat_img, duration, fps):
    frames = []
    h, w = cat_img.shape[:2]
    bg = np.full((h, w, 3), BG_COLOR, dtype=np.uint8)
    center = (w // 2, h // 2)
    total_frames = int(duration * fps)
    for i in range(total_frames):
        angle = (i / total_frames) * 360  # полный оборот
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(cat_img, M, (w, h), borderValue=BG_COLOR)
        mask = cat_img[..., 3] > 0
        frame = bg.copy()
        frame[mask] = rotated[mask][:, :3]
        frames.append(frame)
    return frames


def main():
    if not os.path.exists(STAND_IMG):
        print(f'Файл {STAND_IMG} не найден!')
        return
    cat_img = extract_cat(STAND_IMG)
    frames = create_frames(cat_img, DURATION, FPS)
    clip = ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames], fps=FPS)
    if os.path.exists(AUDIO_FILE):
        audio = AudioFileClip(AUDIO_FILE).subclip(0, DURATION)
        clip = clip.set_audio(audio)
    clip.write_videofile(OUTPUT_VIDEO, codec='libx264', audio_codec='aac')
    print(f'Видео сохранено: {OUTPUT_VIDEO}')

if __name__ == '__main__':
    main()
