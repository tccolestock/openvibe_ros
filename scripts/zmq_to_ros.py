#!/usr/bin/env python

"""
This script receives electrode data from OpenVibe that was transmitted through a ZMQ Pub-Sub protocol. The number of
 electrodes and the samples per epoch are captured and recreated accurately. The recreated data can then be published
 into a ROS topic using the custom message type EegArray. Good for live streaming EEG signals into ROS.

Thomas Colestock
BioRobotics Lab, Florida Atlantic University, 2016
"""
__author__ = "Thomas Colestock"


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
    if samples > 1:
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
