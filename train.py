import sys
import tensorflow as tf

from samples import get_next_batch
from config import *
from cnn import crack_captcha_cnn, X, Y, keep_prob


def log(msg, log_file='tmp.log'):
    with open(log_file, 'a') as f:
        f.write(msg + '\n')
    sys.stdout.write(msg + '\n')


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
        while True:
            batch_x, batch_y = get_next_batch(64)
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            log('[{}] {}'.format(step, loss_))
            # 每100 step计算一次准确率
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch(100)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                log('<--acc--> {}'.format(acc))
                # 如果准确率大于50%,保存模型,完成训练
                if acc > 0.5:
                    saver.save(sess, "./model/crack_capcha.2.model", global_step=step)
                    break
            step += 1

train_crack_captcha_cnn()
