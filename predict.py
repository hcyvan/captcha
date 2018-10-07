import os
import tensorflow as tf
import numpy as np

from cnn import crack_captcha_cnn, X, Y, keep_prob
from config import *
from text import vec2text
from samples import gen_captcha_text_and_image, convert2gray


def crack_captcha(captcha_image):
    output = crack_captcha_cnn()
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint(os.path.dirname(CKPT_PATH)))

        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

        text = text_list[0].tolist()
        vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
        i = 0
        for n in text:
            vector[i * CHAR_SET_LEN + n] = 1
            i += 1
    return vec2text(vector)


def crack_test():
    text, image = gen_captcha_text_and_image(save=False)
    # text, image = get_sina_captcha_text_random()
    image = convert2gray(image)
    image = image.flatten() / 255
    predict_text = crack_captcha(image)
    print("期望: {}  预测: {}".format(text, predict_text))


if __name__ == '__main__':
    crack_test()
