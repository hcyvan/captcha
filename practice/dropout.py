import tensorflow as tf

keep_prob = tf.placeholder(tf.float32)
X = tf.Variable(tf.ones([10,10]))
Y = tf.nn.dropout(X, keep_prob)

with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    print(X)
    result = sess.run(Y, feed_dict={keep_prob: 0.5})
    print(result)
    tf.summary.FileWriter("./board", sess.graph)
