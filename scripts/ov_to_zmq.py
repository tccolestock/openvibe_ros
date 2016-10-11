
# pump an OV sinusoid signal to ros

import zmq
import msgpack


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
            if(type(self.input[0][chunkIndex]) == OVSignalHeader):
                self.signalHeader = self.input[0].pop()
                print("PRINTING SIGNAL HEADER")
                print(self.signalHeader.dimensionLabels)
            if(type(self.input[0][chunkIndex]) == OVSignalBuffer):
                chunk = self.input[0].pop()
                chunk.append(int(self.setting['Number of Channels']))
                chunk.append(int(self.setting['Samples per Epoch']))
                msg = {'signal':chunk, 'labels':self.signalHeader.dimensionLabels}
                print(msg)
                packed = msgpack.dumps(msg)
                socket.send(packed)

    def uninitialize(self):
        return

box = MyOVBox()
