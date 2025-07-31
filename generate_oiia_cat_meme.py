import cv2
import numpy as np
from rembg import remove
from moviepy import ImageSequenceClip, AudioFileClip
from PIL import Image
import os

# --- Конфигурация ---
STAND_IMG = 'stand.png'  # Картинка стоящего кота
SIT_IMG = 'sit.png'      # Картинка сидящего кота
AUDIO_FILE = 'OIIA.mp3' # Музыка (опционально)
OUTPUT_VIDEO = 'oiia_cat_meme.mp4'
FPS = 60
DURATION = 10  # секунд
BG_COLOR = (0, 255, 0)  # Зеленый фон

# --- Вспомогательные функции ---
def extract_cat(img_path):
    img = cv2.imread(img_path)
    img_rgba = remove(img)
    # rembg возвращает PIL.Image, преобразуем в numpy с альфа-каналом
    if isinstance(img_rgba, Image.Image):
        img_rgba = np.array(img_rgba)
    return img_rgba


def resize_cat_rgba(cat_img, out_h, out_w):
    # Масштабируем изображение кота с альфа-каналом до out_h x out_w
    return cv2.resize(cat_img, (out_w, out_h), interpolation=cv2.INTER_AREA)


def create_frames(cat_img, duration, fps, out_h, out_w):
    frames = []
    h, w = cat_img.shape[:2]
    bg = np.full((out_h, out_w, 3), BG_COLOR, dtype=np.uint8)
    total_frames = int(duration * fps)
    cat_rgb = cat_img[..., :3]
    alpha = cat_img[..., 3] / 255.0
    for i in range(total_frames):
        # 3D вращение: имитируем перспективу с помощью сжатия по ширине
        angle = i
        rad = np.deg2rad(angle)
        scale = abs(np.cos(rad)) * 0.7 + 0.05  # ширина меняется
        new_w = max(1, int(w * scale))
        # Масштабируем кота по ширине
        cat_scaled = cv2.resize(cat_rgb, (new_w, h), interpolation=cv2.INTER_AREA)
        alpha_scaled = cv2.resize(alpha, (new_w, h), interpolation=cv2.INTER_AREA)
        # Эмулируем полный оборот: зеркалим изображение, если угол > 180°
        if()
        cat_scaled = cv2.flip(cat_scaled, 1)
        alpha_scaled = cv2.flip(alpha_scaled, 1)
        # Создаем пустой кадр
        frame = bg.copy()
        # Центрируем кота относительно центра видео
        x_offset = (out_w - new_w) // 2
        y_offset = (out_h - h) // 2
        # Вставляем кота с учетом альфа-канала
        for c in range(3):
            frame[y_offset:y_offset+h, x_offset:x_offset+new_w, c] = (
                frame[y_offset:y_offset+h, x_offset:x_offset+new_w, c] * (1 - alpha_scaled) + cat_scaled[:, :, c] * alpha_scaled
            ).astype(np.uint8)
        frames.append(frame)
    return frames


def main():
    if not os.path.exists(STAND_IMG):
        print(f'Файл {STAND_IMG} не найден!')
        return
    if not os.path.exists(SIT_IMG):
        print(f'Файл {SIT_IMG} не найден!')
        return

    stand_cat_img = extract_cat(STAND_IMG)
    sit_cat_img = extract_cat(SIT_IMG)
    if stand_cat_img.shape[2] != 4 or sit_cat_img.shape[2] != 4:
        print('Ошибка: изображения котов должны иметь альфа-канал!')
        return

    # Вычисляем общий размер кадра
    h1, w1 = stand_cat_img.shape[:2]
    h2, w2 = sit_cat_img.shape[:2]
    out_h, out_w = max(h1, h2, 512), max(w1, w2, 512)

    # Масштабируем оба изображения котов к одному размеру
    stand_cat_img = resize_cat_rgba(stand_cat_img, out_h, out_w)
    sit_cat_img = resize_cat_rgba(sit_cat_img, out_h, out_w)

    # 2 секунды стоящего кота (без вращения)
    stand_frames = []
    bg = np.full((out_h, out_w, 3), BG_COLOR, dtype=np.uint8)
    cat_rgb = stand_cat_img[..., :3]
    alpha = stand_cat_img[..., 3] / 255.0
    for _ in range(int(2 * FPS)):
        frame = bg.copy()
        x_offset = 0
        y_offset = 0
        for c in range(3):
            frame[y_offset:y_offset+out_h, x_offset:x_offset+out_w, c] = (
                frame[y_offset:y_offset+out_h, x_offset:x_offset+out_w, c] * (1 - alpha) + cat_rgb[:, :, c] * alpha
            ).astype(np.uint8)
        stand_frames.append(frame)

    # 3 секунды сидящего вращающегося кота
    spin_frames = create_frames(sit_cat_img, 3, FPS, out_h, out_w)

    frames = stand_frames + spin_frames

    clip = ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames], fps=FPS)
    if os.path.exists(AUDIO_FILE):
        audio = AudioFileClip(AUDIO_FILE).subclipped(0, 5)
        clip = clip.with_audio(audio)
    clip.write_videofile(OUTPUT_VIDEO, codec='libx264', audio_codec='aac')
    print(f'Видео сохранено: {OUTPUT_VIDEO}')

if __name__ == '__main__':
    main()
