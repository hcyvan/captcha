import time
import tensorflow as tf

from samples import get_next_batch
from config import *
from cnn import crack_captcha_cnn, X, Y, keep_prob
from log import log


def train_crack_captcha_cnn():
    output = crack_captcha_cnn()
    # loss
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    predict = tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        step = 0
        start = time.time()
        while True:
            batch_x, batch_y = get_next_batch(64)
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            log('step:{} loss:{}'.format(step, loss_), start)
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch(100)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                log('step:{} ----accuracy:{}'.format(step, acc), start)
                if acc > 0.95:
                    saver.save(sess, './model/sina95/sina.capcha', global_step=step)
                    break
                if acc > 0.9:
                    saver.save(sess, './model/sina90/sina.capcha', global_step=step)
                elif acc > 0.8:
                    saver.save(sess, './model/sina80/sina.capcha', global_step=step)
            step += 1
    tf.summary.FileWriter(BOARD_PATH, sess.graph)


train_crack_captcha_cnn()
