from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection

import time

class PlayerDetectionNet:

        def input_image_size(self):
            return (64,64)

        def __init__(self):

            net = FeedForwardNetwork()
            inLayer = LinearLayer(64*64*3)
            hiddenLayer1 = SigmoidLayer(250)
            hiddenLayer2 = SigmoidLayer(100)
            outLayer = LinearLayer(1)

            net.addInputModule(inLayer)
            net.addModule(hiddenLayer1)
            net.addModule(hiddenLayer2)
            net.addOutputModule(outLayer)

            in_to_hidden = FullConnection(inLayer, hiddenLayer1)
            hth = FullConnection(hiddenLayer1, hiddenLayer2)
            hidden_to_out = FullConnection(hiddenLayer2, outLayer)

            net.addConnection(in_to_hidden)
            net.addConnection(hth)
            net.addConnection(hidden_to_out)

            net.sortModules()
            self.net = net

        def activate(self, input):
            arr = [ord(x) for x in (list(input))]
            return self.net.activate(arr);

        def train_on_dataset(self, dataset, max_epochs = 10):
            trainer = BackpropTrainer(self.net, dataset=dataset, learningrate=0.01, momentum=0.04, verbose=True, weightdecay=0.01)
            trainer.trainUntilConvergence(maxEpochs=max_epochs, verbose=True)#, continueEpochs, validationProportion);
            #error = trainer.train()

            NetworkWriter.writeToFile(self.net, ("./network_%d.xml")%(time.time()))
            return 0
