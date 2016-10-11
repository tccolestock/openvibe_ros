
# pump an OV sinusoid signal to ros

# import rospy
import zmq
import msgpack
# from std_msgs.msg import UInt32
#
#
# rospy.init_node("ov_to_ros", anonymous=True)
# pub_handle = rospy.Publisher("ovout", UInt32, queue_size=10)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signalHeader = None
        self.x = 3

    def initialize(self):
        return

    def process(self):
        for chunkIndex in range(len(self.input[0])):
            if(type(self.input[0][chunkIndex]) == OVSignalBuffer):
                chunk = self.input[0].pop()
                chunk.append(int(self.setting['Number of Channels']))
                chunk.append(int(self.setting['Samples per Epoch']))
            # pub_handle.publish(self.x)
                # print(self.x)
                print(chunk)
                # print(chunk[2])
                # packed = msgpack.dumps(self.x)
                packed = msgpack.dumps(chunk)
                socket.send(packed)

    def uninitialize(self):
        return

box = MyOVBox()
