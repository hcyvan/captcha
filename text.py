import numpy as np
from config import *


def text2vec(text):
    text_len = len(text)
    if text_len > MAX_CAPTCHA:
        raise ValueError('Captcha Overflow')
    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    for i, c in enumerate(text):
        idx = i * CHAR_SET_LEN + CHAR_SET.index(c)
        vector[idx] = 1
    return vector


def vec2text(vec):
    text = ''
    for char_vec in vec.reshape([-1, CHAR_SET_LEN]):
        vector = char_vec.tolist()
        if 1 in vector:
            text = text + CHAR_SET[vector.index(1)]
    return text
