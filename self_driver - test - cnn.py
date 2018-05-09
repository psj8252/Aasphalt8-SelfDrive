from PIL import ImageGrab, Image
from getkeys import key_check
from sendkey import PressKey
from sendkey import ReleaseKey
from time import sleep
import tensorflow as tf
import cv2
import numpy as np
import pandas as pd


hidden_size = 4  # output from the LSTM. 5 to directly predict one-hot
batch_size = 100   # one sentence
data_mean = 17.119790415671556
data_std = 63.36037302373175

A = 0x1E
S = 0x1F
D = 0x20
SPACE = 0x39


X = tf.placeholder(tf.float32, [None, 200, 400, 1])
Y = tf.placeholder(tf.float32, [None, 4])

with tf.variable_scope("cnn"):
    
    # conv : 5, 200, 400, 16
    conv = tf.layers.conv2d(inputs=X, filters=16, kernel_size=[4, 8], padding='SAME', activation=tf.nn.relu)
    # pool : 5, 50, 99, 16
    pool = tf.layers.max_pooling2d(inputs=conv, pool_size=[2, 4], padding='SAME', strides=1)
    # conv2 
    conv2 = tf.layers.conv2d(inputs=X, filters=64, kernel_size=[4, 8], padding='SAME', activation=tf.nn.relu)
    # pool2 
    pool2 = tf.layers.max_pooling2d(inputs=conv, pool_size=[4, 8], padding='SAME', strides=2)
    # conv3
    conv2 = tf.layers.conv2d(inputs=X, filters=128, kernel_size=[4, 8], padding='SAME', activation=tf.nn.relu)
    # pool3 
    pool3 = tf.layers.max_pooling2d(inputs=conv, pool_size=[4, 8], padding='SAME', strides=2)
    
    flat = tf.reshape(pool3, [-1, 100*200*16])
    w = tf.get_variable("w", [hidden_size, hidden_size])
    b = tf.get_variable("b", [hidden_size])
    
    logit = tf.layers.dense(inputs=flat, units=4)
    outputs = tf.sigmoid(tf.matmul(logit, w) + b)
    predict = outputs - [0.2, 0.05,0.25 , 0.1] > 0
    

saver = tf.train.Saver()

model = input("Drive Model Name: ")
for i in range(5):
    print(i+1)
    sleep(1)


with tf.Session() as sess:
    saver.restore(sess, "./model/"+model+".ckpt")

    data_df = pd.read_csv('log.csv', names=['name','key_out'])
    names = data_df['name'].values
    name_i = 0
    key_out = [eval(x) for x in data_df['key_out'].values]

    while True:

        img = Image.open("./img/"+names[name_i])
##        snapshot = np.array(ImageGrab.grab())
##        _img = cv2.resize(snapshot, (400,200),interpolation=cv2.INTER_AREA)
##        img = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)
##        img = cv2.Canny(img, threshold1 = 250, threshold2=200)

        data = np.array( img, dtype='uint8' ).reshape([1,200,400,1])
        data = (data-data_mean) / data_std

        result, pred = sess.run([outputs, predict], feed_dict={X:data})
        #x = sess.run(outputs, feed_dict={X:data})
        print(key_out[name_i], [int(a*100)/100 for a in result[0]], pred)
##        ReleaseKey(A)
##        ReleaseKey(D)
##        ReleaseKey(SPACE)
##        ReleaseKey(S)
        #print(x, key_out[name_i], [int(a*100)/100 for a in sess.run(outputs, feed_dict={X:data})])
        name_i += 1
##        if acts[1]:
##            PressKey(S)
##        if acts[0]:
##            PressKey(A)
##        if acts[2]:
##            PressKey(D)
##        if acts[3]:
##            PressKey(SPACE)



        