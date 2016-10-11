#!/usr/bin/env python

import rospy
import zmq
import msgpack
from std_msgs.msg import UInt32


rospy.init_node("ov_to_ros", anonymous=True)
pub_handle = rospy.Publisher("ovout", UInt32, queue_size=10)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt(zmq.SUBSCRIBE, b'')


while not rospy.is_shutdown():
    recvd = socket.recv()
    msg = msgpack.loads(recvd)
    samples = int(msg.pop())  # 'number of samples per epoch'
    if (samples > 1):
        channels = int(msg.pop())  # 'number of channels'
        for i in range(samples):
            x = []
            for j in range(channels):
                x.append(msg[i+(j*samples)])
            print(msg)
            print(x)  # will end up with as many arrays as there are
            # samples per epoch of length channels.
            # Import data from x into msg object and publish here.
            # pub_handle.publish(msg)
    print("not more than one sample")
    print(msg)
