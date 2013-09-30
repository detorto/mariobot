class MyNet:
        def __init__(self):
            print "building network"
            net = FeedForwardNetwork()
            inLayer = LinearLayer(64*64*3)
            hiddenLayer1 = SigmoidLayer(100)
            hiddenLayer2 = SigmoidLayer(50)
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

        def generate_dataset(self):

            posfc = FileCapturer();
            posfc.start_capture("./train_sets/pos_data/")
            
            negfc = FileCapturer();
            negfc.start_capture("./train_sets/neg_data/")

            pos_image = posfc.get_last_frame_pil();
            neg_image = negfc.get_last_frame_pil();

            self.dataset = SupervisedDataSet(64*64*3, 1)

            while pos_image and neg_image:
                arr1 = [ord(x) for x in (list(pos_image.tostring()))]
                self.dataset.addSample(arr1, (1,))

                arr2 = [ord(x) for x in (list(neg_image.tostring()))]
                self.dataset.addSample(arr1, (0,))

        def train_on_ready_dataset(self):
            trainer = BackpropTrainer(net, dataset=self.dataset, learningrate=0.01, momentum=0.04, verbose=True, weightdecay=0.01)
            trainer.trainUntilConvergence(maxEpochs=10, verbose=True)#, continueEpochs, validationProportion);
            NetworkWriter.writeToFile(net, ("./network_OOOK!.xml"))
     