import os
import random
from captcha.image import ImageCaptcha
from PIL import Image
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
    return captcha_text


class SinaCaptcha(ImageCaptcha):
    def __init__(self):
        super().__init__(fonts=['./font/comic_andy.ttf'], width=IMAGE_WIDTH, height=IMAGE_HEIGHT, font_sizes=[28])

    @staticmethod
    def create_noise_dots(image, color, width=3, number=30):
        return image


def gen_captcha_text_and_image(save=True, sample_dir=SAMPLE_DIR):
    image = SinaCaptcha()
    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text)
    img = image.generate(captcha_text)
    if save:
        image.write(captcha_text, os.path.join(sample_dir, captcha_text + '.png'))
    else:
        img = Image.open(img)
        img = np.array(img)
        return captcha_text, img


def get_sina_captcha_text_random():
    sample_dir = './sina/test_resize'
    pics = list(os.listdir(sample_dir))
    pic = random.choice(pics)
    img = Image.open(os.path.join(sample_dir, pic))
    return pic.split('.')[0], np.array(img)


def convert2gray(img):
    if len(img.shape) > 2:
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img


def get_next_batch(batch_size=128):
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])
    def wrap_gen_captcha_text_and_image():
        while True:
            text, image = gen_captcha_text_and_image(False)
            if image.shape == (IMAGE_HEIGHT, IMAGE_WIDTH, 3):
                return text, image

    for i in range(batch_size):
        text, image = wrap_gen_captcha_text_and_image()
        image = convert2gray(image)

        batch_x[i, :] = image.flatten() / 255
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y


if __name__ == '__main__':
    gen_captcha_text_and_image()
