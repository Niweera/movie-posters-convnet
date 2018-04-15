#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import numpy as np
from functools import reduce
from operator import mul

from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.vgg16 import VGG16

import utils
import db_manager


# Variable specific to vgg-16/vgg-19
img_width = 224
img_height = 224


# Feature extractor
def get_features(model, data, db):
    n_posters = len(data)
    features = []
    for i, poster in enumerate(data):
        print('getting features for {} {}/{}'.format(
            poster.path_img, i+1, n_posters))
        # Resize image to be 224x224
        img = image.load_img(poster.path_img,
                             target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        y = model.predict(x)
        # Vectorize the 7x7x512 tensor
        poster.features = y.reshape(reduce(mul, y.shape, 1))
        db.commit()
    return data


def load_model(config):
    if config['features']['model'] == 'vgg16':
        return VGG16(weights='imagenet', include_top=False)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args.config)
    config = utils.read_config('./config/development.conf')
    # Load VGG16, guys you better have a GPU...
    model = load_model(config)
    data, db = db_manager.get_all_data(config['general']['db_uri'])

    data_features = get_features(model, data, db)
    db.commit()
    return data_features


if __name__ == "__main__":
    main(sys.argv[1:])
