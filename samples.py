import os
import random
from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np

from config import *
from text import text2vec

SAMPLE_DIR = './images/sample'


def random_captcha_text(captcha_size=MAX_CAPTCHA):
    char_set = string.digits + string.ascii_letters
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return ''.join(captcha_text)


class SinaCaptcha(ImageCaptcha):
    def __init__(self):
        super().__init__(fonts=['./font/comic_andy.ttf'], width=IMAGE_WIDTH, height=IMAGE_HEIGHT, font_sizes=[28])

    @staticmethod
    def create_noise_dots(image, color, width=3, number=30):
        return image


def gen_captcha_text_and_image(save=True, sample_dir=SAMPLE_DIR):
    image = SinaCaptcha()
    captcha_text = random_captcha_text()
    img = image.generate(captcha_text)
    if save:
        image.write(captcha_text, os.path.join(sample_dir, captcha_text + '.png'))
    else:
        img = Image.open(img)
        img = np.array(img)
        return captcha_text, img


def gen_sina_captcha_text_and_image(save=True):
    img = Image.new('RGB', (100, 40), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # draw text
    font_name = 'PlaytimeWithHotToddies3D.ttf'
    font = ImageFont.truetype('./font/' + font_name, 32)
    txt = random_captcha_text()
    draw.text((5, 0), txt, font=font, fill=(0, 0, 255))
    # draw line
    begin = (random.randint(0, 20), random.randint(0, 40))
    end = (random.randint(80, 100), random.randint(0, 40))
    draw.line([begin, end], fill=(0, 0, 255))
    # rotate
    img = img.rotate(random.randint(-5, 5), fillcolor=(255, 255, 255), resample=Image.BICUBIC)
    if save:
        img.save('./test.png')
        img_array = np.array(img)
        img_array = convert2double(img_array)
        img_gray = Image.fromarray(img_array.astype('uint8')).convert('RGB')
        img_gray.save('./test2.png')
    else:
        # img.save('./test.png')
        return txt, np.array(img)


def get_sina_captcha_text_random():
    sample_dir = './images/sina/test'
    pics = list(os.listdir(sample_dir))
    pic = random.choice(pics)
    img = Image.open(os.path.join(sample_dir, pic))
    img = img.convert('RGB')
    return pic.split('.')[0], np.array(img)


def convert2gray(img):
    if len(img.shape) > 2:
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img


def convert2double(img):
    def to_double(black):
        for i in range(len(black)):
            for j in range(len(black[0])):
                if black[i][j] < 230:
                    black[i][j] = 0
                else:
                    black[i][j] = 255
        return black
    if len(img.shape) > 2:
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        img = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return to_double(img)
    else:
        return img


def get_next_batch(batch_size=128):
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])

    def wrap_gen_captcha_text_and_image():
        while True:
            text, image = gen_sina_captcha_text_and_image(False)
            # text, image = gen_captcha_text_and_image(False)
            if image.shape == (IMAGE_HEIGHT, IMAGE_WIDTH, 3):
                return text, image

    for i in range(batch_size):
        text, image = wrap_gen_captcha_text_and_image()
        image = convert2double(image)
        batch_x[i, :] = image.flatten() / 255
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y


if __name__ == '__main__':
    # gen_cap?tcha_text_and_image()
    # gen_sina_captcha_text_and_image(False)
    txt, img = get_sina_captcha_text_random()
    img_array = convert2double(img)
    img_gray = Image.fromarray(img_array.astype('uint8')).convert('RGB')
    img_gray.save('./test2.png')
    print(txt)
