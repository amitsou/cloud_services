import os
import cv2
import sys
import json
import time
import codecs
import argparse
import logging
import numpy as np
import warnings

try:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=FutureWarning)
        from keras.models import load_model
        from keras.preprocessing import image
        from keras import layers
        from keras import models
        from keras import regularizers
        from keras import layers
        from keras.preprocessing.image import ImageDataGenerator
except Exception as ex:
    sys.exit('Error import Keras library')

try:
    import paho.mqtt.client as mqtt
except Exception as ex:
    sys.exit('Paho library is not present')


def motion_clf(msg):
    #Reconstructing image
    height, width, channels, data_in = decode_json_msg(msg)
    reconstruct_img(height, width, channels, data_in)
    predict_image(image)


def get_model():
    model_dir = "/myfolder/" #enter your folder's name
    model_name = "new51Classes.h5" #enter your model's name
    model_dir = os.path.join(model_dir,model_name)
    return model_dir


def reconstruct_img(height, width, channels, data_in):
    image = data_in.reshape((height,width,channels)) #Rehape 1D to 2D
    image = np.expand_dims(image, axis=0) #Convert shape to 4D
    return image


def predict_image(img):
    model = load_model(get_model())
    model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
    model.layers[0].input_shape

    pred = str(model.predict(img))
    client.publish(out_topic,pred)


def decode_json_msg(msg):
    """Decode json message on platform

    Args:
        msg (str): The published message on a specific topic
    """
    m_decode = str(msg.payload.decode("utf-8","ignore"))
    tmp = json.loads(m_decode)
    data_in = np.array(tmp[0])

    height = tmp[1]
    width = tmp[2]
    channels = tmp[3]
    return height, width, channels, data_in


def p_type_service_args():
    """Provide the P-type service args
    """
    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument("--username", metavar='username(text)', help="Please provide username")
    parser.add_argument("--input_topics", nargs='*', metavar='Input_topic', help='MQTT Broker Input Topics')
    parser.add_argument("--output_topics",nargs='*',metavar='Output_topic',help='MQTT Broker Output Topics')
    parser.add_argument("--p", metavar='password(text)', help="Please provide password")

    args = parser.parse_args()
    username=args.username
    user_pass=args.p
    in_topics = args.input_topics
    in_topic = in_topics[0]
    out_topics = args.output_topics
    out_topic = out_topics[0]

    return username, user_pass, in_topic, out_topic