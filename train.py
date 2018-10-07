import sys
import datetime
import time
import tensorflow as tf

from samples import get_next_batch
from config import *
from cnn import crack_captcha_cnn, X, Y, keep_prob


def log(msg, start=None):
    def get_progress_time(s):
        h = s // 3600
        s = s % 3600
        m = s // 60
        s = s % 60
        return (h, m, s)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if start:
        delta_time = get_progress_time(int(time.time() - start))
        ts = str(delta_time[0]) + 'h' + str(delta_time[1]) + 'm' + str(delta_time[2]) + 's'
        log_msg = '{} training:{} {}'.format(time_now, ts, msg)
    else:
        log_msg = '{} {}'.format(time_now, msg)
    with open(LOG_PATH, 'a') as f:
        f.write(log_msg + '\n')
    sys.stdout.write(log_msg + '\n')


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
                log('step:{} ----accuracy {}'.format(step, acc), start)
                if acc > STOP_ACC:
                    saver.save(sess, CKPT_PATH, global_step=step)
                    break
            step += 1
    tf.summary.FileWriter(BOARD_PATH, sess.graph)


train_crack_captcha_cnn()
