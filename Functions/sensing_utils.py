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



def upload_image(out_topic):
    """Upload an image into the Synaisthisi Platform
    """
    try:
        while True:

            img_dir = get_img_dir()
            data_out = parse_img(img_dir)
            client.publish(out_topic, data_out)

    except KeyboardInterrupt:
            client.loop_stop()


def get_img_dir():
    """Get the image path

    Returns:
        [str]: [The absolute path to the image file]
    """
    img_dir = '' #enter your image path here
    img_name = ''#enter image name here
    img_dir = os.path.join(img_dir,img_name)
    return img_dir


def parse_img(img_dir):
    """Open, preprocess and convert an image into json format

    Args:
        img_dir (str): The image absolute path

    Returns:
        [str]: The json object to be published to the platform
    """
    img = cv2.imread(img_dir)
    height, width, channels = img.shape
    img = image.load_img(img_dir, target_size=(height,width))
    img = np.array(image)
    img = img.ravel()

    compressed_obj = [img.tolist(), height, width, channels]
    json_obj = json.dumps(compressed_obj)
    return json_obj


def s_type_service_args():
    """
    Provide the S-type service args
    """
    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument("--username", metavar='username(text)', help="Please provide username")
    parser.add_argument("--p", metavar='password(text)', help="Please provide password")
    parser.add_argument("--output_topics", nargs='*', metavar='Output_topic',help='MQTT Broker Output Topics')

    #Developer should take care to parse as many input/output topics created in web app
    args = parser.parse_args()
    username = args.username
    user_pass = args.p
    out_topics = args.output_topics

    print("Output Topics: {0}".format(out_topics))
    out_topic = out_topics[0]
    return username, user_pass, out_topic