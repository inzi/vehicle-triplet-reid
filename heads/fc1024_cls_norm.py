import tensorflow as tf
from tensorflow.contrib import slim

def head(endpoints, embedding_dim, is_training):
    endpoints['head_output'] = slim.fully_connected(
        endpoints['model_output'], 1024, normalizer_fn=slim.batch_norm,
        normalizer_params={
            'decay': 0.9,
            'epsilon': 1e-5,
            'scale': True,
            'is_training': is_training,
            'updates_collections': tf.GraphKeys.UPDATE_OPS,
        })

    endpoints['emb'] = endpoints['emb_raw'] = slim.fully_connected(
        endpoints['head_output'], embedding_dim, activation_fn=None,
        weights_initializer=tf.orthogonal_initializer(), scope='emb')
    endpoints['emb'] = tf.nn.l2_normalize(endpoints['emb_raw'], -1)

    endpoints['model_logits'] = endpoints['model_raw'] = slim.fully_connected(
        endpoints['model_output'], 1232, activation_fn=None,
        weights_initializer=tf.orthogonal_initializer(), scope='model_cls')

    endpoints['color_logits'] = endpoints['color_raw'] = slim.fully_connected(
        endpoints['model_output'], 11, activation_fn=None,
        weights_initializer=tf.orthogonal_initializer(), scope='color_cls')

    return endpoints
