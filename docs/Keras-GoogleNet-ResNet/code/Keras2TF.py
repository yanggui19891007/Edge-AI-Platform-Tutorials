'''
 - "How to convert trained Keras model to a single TensorFlow .pb file and make prediction" available from https://github.com/Tony607/keras-tf-pb

 - Modified by daniele.bagni@xilinx.com
 - last change on 12 Jun2 2019
'''

# USAGE
# python Keras2TFy -c miniVggNet -d cifar10

import os
import sys
import shutil
from keras import backend as K
#from tensorflow.keras.models import model_from_json
from keras.models import load_model
import tensorflow as tf

import argparse #DB
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n",  "--network", default="LeNet",          help="input CNN")
ap.add_argument("-d",  "--dataset", default="fashion-mnist",  help="input dataset")
args = vars(ap.parse_args())
cnn_name = args["network"]
dataset_name = args["dataset"]

if (dataset_name == "cifar10") :
    from config import cifar10_config as cfg #DB
else:
    from config import fashion_mnist_config as cfg #DB

    
##############################################
# Set up directories
##############################################

KERAS_MODEL_DIR = cfg.KERAS_MODEL_DIR #DB

WEIGHTS_DIR = os.path.join(KERAS_MODEL_DIR, cnn_name)

CHKPT_MODEL_DIR = cfg.CHKPT_MODEL_DIR


# set learning phase for no training: This line must be executed before loading Keras model
K.set_learning_phase(0)

# load weights & architecture into new model
model = load_model(os.path.join(WEIGHTS_DIR,"best_chkpt.hdf5"))

#print the CNN structure
model.summary()

# make list of output node names
output_names=[out.op.name for out in model.outputs]

# set up tensorflow saver object
saver = tf.train.Saver()

# fetch the tensorflow session using the Keras backend
sess = K.get_session()

# get the tensorflow session graph
graph_def = sess.graph.as_graph_def()


# Check the input and output name
print ("\n TF input node name:")
print(model.inputs)
print ("\n TF output node name:")
print(model.outputs)

# write out tensorflow checkpoint & inference graph (from MH's "MNIST classification with TensorFlow and Xilinx DNNDK")
save_path = saver.save(sess, os.path.join(CHKPT_MODEL_DIR, cnn_name, "float_model.ckpt"))
tf.train.write_graph(graph_def, os.path.join(CHKPT_MODEL_DIR, cnn_name), "infer_graph.pb", as_text=False)


print ("\nFINISHED CREATING TF FILES\n")
