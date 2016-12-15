#!/usr/bin/env python

import rospy
import zmq
import msgpack

from std_msgs.msg import UInt32
from openvibe_ros.msg import EegArray


rospy.init_node("ov_to_ros", anonymous=True)
eegPub = rospy.Publisher("eeg", EegArray, queue_size=10)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt(zmq.SUBSCRIBE, b'')
eeg = EegArray()

while not rospy.is_shutdown():
    print(eeg)
    recvd = socket.recv()
    msg = msgpack.loads(recvd)
    print(msg)
    signal = msg['signal']
    samples = int(signal.pop())  # 'number of samples per epoch'
    channels = int(signal.pop())  # 'number of channels'
    labels = msg['labels'][0:channels]
    if (samples > 1):
        for i in range(samples):
            x = []
            for j in range(channels):
                x.append(signal[i+(j*samples)])
            eeg.data = x
            eeg.header.stamp = rospy.Time.now()
            eeg.header.frame_id = 'eeg'
            eeg.channels = labels
            print(eeg)
            eegPub.publish(eeg)
    else:
        eeg.data = signal
        eeg.header.stamp = rospy.Time.now()
        eeg.header.frame_id = 'eeg'
        eeg.channels = labels
        print(eeg)
        eegPub.publish(eeg)
    # print("not more than one sample")
    # print(msg)
