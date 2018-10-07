import tensorflow as tf

input_v = tf.constant([[
    [[1,1], [2,2], [3,3]],
    [[4,4], [5,5], [6,6]],
    [[7,7], [8,8], [9,9]]]], dtype=tf.float32)

filter_v = tf.constant([
    [[[1],[1]], [[2],[1]]],
    [[[3],[1]], [[4],[1]]]], dtype=tf.float32)
op = tf.nn.conv2d(input_v, filter_v, strides=[1, 1, 1, 1], padding='VALID')
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    result = sess.run(op)
    print(result)
    print(result.shape)
    tf.summary.FileWriter("./board", sess.graph)

