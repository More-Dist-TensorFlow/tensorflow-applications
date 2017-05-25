import tensorflow as tf

import paho.mqtt.client as mqtt
import numpy as np
import json
import curses

BROKER = "[broker-address]"
TOPIC = "[subscribe-topic]"
QUEUE_SIZE = 10

mq5 = np.array([])
mq7 = np.array([])
mq131 = np.array([])
mq135 = np.array([])

mq5_average = 0
mq7_average = 0
mq131_average = 0
mq135_average = 0

sess = tf.Session()
mq5_variable = tf.Variable(0,dtype=tf.float64, name='mq5_variable')
mq7_variable = tf.Variable(0, name='mq7_variable')
mq131_variable = tf.Variable(0, name='mq131_variable')
mq135_variable = tf.Variable(0, name='mq135_variable')

sess.run(tf.global_variables_initializer())

'''placeholder'''
item = tf.placeholder(tf.float32, name='item')
size = tf.placeholder(tf.float32, name='size')

'''MQ5 OPERATORS'''
mq5_sum_variable = tf.Variable(0.0, name='mq5_sum_variable')
mq5_average_variable =  tf.Variable(0.0, name='mq5_average_variable')

mq5_op_add = tf.add(item, mq5_sum_variable, name="mq5_op_add")
assign_mq5_add = tf.assign(mq5_sum_variable, mq5_op_add)

mq5_op_divide = tf.divide(mq5_sum_variable, size, name="mq5_op_divide")
assign_mq5_divide = tf.assign(mq5_average_variable, mq5_op_divide)

'''MQ7 OPERATORS'''
mq7_sum_variable = tf.Variable(0.0, name='mq7_sum_variable')
mq7_average_variable =  tf.Variable(0.0, name='mq7_average_variable')

mq7_op_add = tf.add(item, mq7_sum_variable, name="mq7_op_add")
assign_mq7_add = tf.assign(mq7_sum_variable, mq7_op_add)

mq7_op_divide = tf.divide(mq7_sum_variable, size, name="mq7_op_divide")
assign_mq7_divide = tf.assign(mq7_average_variable, mq7_op_divide)

'''MQ131 OPERATORS'''
mq131_sum_variable = tf.Variable(0.0, name='mq131_sum_variable')
mq131_average_variable =  tf.Variable(0.0, name='mq131_average_variable')

mq131_op_add = tf.add(item, mq131_sum_variable, name="mq131_op_add")
assign_mq131_add = tf.assign(mq131_sum_variable, mq131_op_add)

mq131_op_divide = tf.divide(mq131_sum_variable, size, name="mq131_op_divide")
assign_mq131_divide = tf.assign(mq131_average_variable, mq131_op_divide)

'''MQ135 OPERATORS'''
mq135_sum_variable = tf.Variable(0.0, name='mq135_sum_variable')
mq135_average_variable =  tf.Variable(0.0, name='mq135_average_variable')

mq135_op_add = tf.add(item, mq135_sum_variable, name="mq135_op_add")
assign_mq135_add = tf.assign(mq135_sum_variable, mq135_op_add)

mq135_op_divide = tf.divide(mq135_sum_variable, size, name="mq135_op_divide")
assign_mq135_divide = tf.assign(mq135_average_variable, mq135_op_divide)


def mq5_result(value):
    global mq5
    global mq5_average
    sess.run(tf.global_variables_initializer())

    if mq5.size == QUEUE_SIZE:
        mq5 = mq5[1:]
        mq5 = np.append(mq5, value)
    else:
        mq5 = np.append(mq5, value)

    for index, mq5_item in enumerate(mq5):
        result = sess.run(assign_mq5_add, feed_dict={item:value})

    mq5_average = sess.run(assign_mq5_divide, feed_dict={size:mq5.size})
    result_print()


def mq7_result(value):
    global mq7
    global mq7_average
    sess.run(tf.global_variables_initializer())

    if mq7.size == QUEUE_SIZE:
        mq7 = mq7[1:]
        mq7 = np.append(mq7, value)
    else:
        mq7 = np.append(mq7, value)

    for index, mq7_item in enumerate(mq7):
        result = sess.run(assign_mq7_add, feed_dict={item:value})

    mq7_average = sess.run(assign_mq7_divide, feed_dict={size:mq7.size})
    result_print()


def mq131_result(value):
    global mq131
    global mq131_average
    sess.run(tf.global_variables_initializer())

    if mq131.size == QUEUE_SIZE:
        mq131 = mq131[1:]
        mq131 = np.append(mq131, value)
    else:
        mq131 = np.append(mq131, value)

    for index, mq131_item in enumerate(mq131):
        result = sess.run(assign_mq131_add, feed_dict={item:value})

    mq131_average = sess.run(assign_mq131_divide, feed_dict={size:mq131.size})
    result_print()


def mq135_result(value):
    global mq135
    global mq135_average
    sess.run(tf.global_variables_initializer())

    if mq135.size == QUEUE_SIZE:
        mq135 = mq135[1:]
        mq135 = np.append(mq135, value)
    else:
        mq135 = np.append(mq135, value)

    for index, mq135_item in enumerate(mq135):
        result = sess.run(assign_mq135_add, feed_dict={item:value})
    
    mq135_average = sess.run(assign_mq135_divide, feed_dict={size:mq135.size})
    result_print()


def result_print():
    global mq5_average
    global mq7_average
    global mq131_average
    global mq135_average
              
    stdscr.addstr(0, 0,"========SCALE========")
    stdscr.addstr(1, 0, "Average MQ5  : " + str(mq5_average))
    stdscr.addstr(2, 0, "Average MQ7  : " + str(mq7_average))
    stdscr.addstr(3, 0, "Average MQ131: " + str(mq131_average))
    stdscr.addstr(4, 0, "Average MQ135: " + str(mq135_average))
    stdscr.refresh()


def json_parse(msg):
    data = json.loads(msg)
    event = data['d']['event']
    value = data['d']['value']
    return event, value

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    event, value = json_parse(msg.payload)

    if event == "pollution_air_mq5":
        mq5_result(value)
    elif event == "pollution_air_mq7":
        mq7_result(value)
    elif event == "pollution_air_mq131":
        mq131_result(value)
    elif event == "pollution_air_mq135":
        mq135_result(value)



if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        client.loop_forever()
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
