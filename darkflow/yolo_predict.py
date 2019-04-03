# General Utilities
import re
import os
import sys
import csv
import random
import subprocess
from PIL import Image
from PIL import ImageDraw
import argparse
from tqdm import tqdm
from os import listdir
from os.path import isfile, join

# ML / Deep learning Utilities
from darkflow.net.build import TFNet
import cv2
import numpy as np
from numpy import loadtxt
import pandas as pd
import matplotlib.pyplot as plt

# Helper function to create a new folder
def mkdir(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
        else:
            print("(%s) already exists" % (path))

##################
### PREDICTION ###
##################
def predict(img_paths, model_cfg, thresh, save_dir):
    '''
        FUNCTION: To make bounding box object detection predictions given list of image paths

        Parameters
        ----------
        img_paths: (list) List of the paths to each image that needs to be fed through model for prediction
        model_cfg: (str) The path to the model configuration file 
        thresh: (float) Threshold for making a bounding box prediction
        save_dir: (str) Directory to save the predicted images to

        Returns
        -------
        Nothing. Saves all images with bounding boxes to specified directory.
    '''
    options = {"model": model_cfg, 
               "load": -1,
               "threshold": thresh}

    # Setting the tensorflow graph
    tfnet = TFNet(options)
    
    # List of those that are predicted not to have any store signs
    no_sign = []

    # List of those that are predicted to have store signs
    with_sign = []
    
    # Looping through each image and making a prediction
    for img_path in tqdm(img_paths):
        
        img = cv2.imread(img_path)
        
        results = tfnet.return_predict(img)

        if not results:
            print('{} : No store signs have been found here ...'.format(img_path))
            no_sign.append(img_path)
        else:
            # Get a list of random colors if multiple 
            # bounding boxes need to be printed
            colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

            # Finding the highest confidence bounding
            # box
            max_confidence = 0
            box = None
            for x in results:
                if x['confidence'] > max_confidence:
                    max_confidence = x['confidence']
                    box = x
                    
            print('{} : Store sign has been found here with confidence of {}'.format(img_path, max_confidence))
            with_sign.append(img_path)

            # Pasting bounding box with highest confidence level 
            # on original image and saving it
            tl = (box['topleft']['x'], box['topleft']['y'])
            br = (box['bottomright']['x'], box['bottomright']['y'])
            label = box['label']
            confidence = box['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            img_pred = cv2.rectangle(img, tl, br, colors[0], 5)
            img_pred = cv2.putText(img, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

            Image.fromarray(img_pred).save(join(save_dir, '{}_{}.jpg'.format(img_path[:-img_path.rfind('.')], 'bb')))

    # Saving which of those images are predicted to have store signs 
    # or not
    with open(join(save_dir, './predict_info/no_sign.csv'), 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(no_sign)
        
    with open(join(save_dir, './predict_info/with_sign.csv'), 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(with_sign)

############
### MAIN ###
############
if __name__ == '__main__':
    
    ##########################
    ### READING ARG PARAMS ###
    ##########################
    # Read in arguments from command line
    parser = argparse.ArgumentParser(
        description='Predicts the bounding box for store sign.'
    )
    parser.add_argument('data_dir', metavar='DATA-DIRECTORY', action='store', help='Path to the data directory with the sliding window images from the original panoramic images.')
    parser.add_argument('--save_dir', metavar='SAVE-DIRECTORY', action='store', help='Set directory to save all the images that are likely to have a store sign predicted by YOLO.')
    parser.add_argument('--model_cfg', metavar='MODEL-CONFIGURATION', action='store', help='Sets path to the .cfg file to be used for re-building model to run predictions and loads last checkpoint in ./ckpt folder for model prediction. Default: ./cfg/tiny-yolo-voc-liquor.cfg ')
    parser.add_argument('--thresh', metavar='THRESHOLD', action='store', help='Sets the minimum threshold required for making a bounding box prediction. Default: 0.5')
    settings = parser.parse_args()
    
    ###########################
    ### PREDICTION HANDLING ###
    ###########################
    # Store all the image paths into list
    image_paths = [join(settings.data_dir, f) for f in listdir(settings.data_dir) if isfile(join(settings.data_dir, f)) and f[-3:] == 'jpg' or f[-3:] == 'png']
    
    # Set model configuration file
    if settings.model_cfg != None:
        model_cfg = settings.model_cfg
    else:
        model_cfg = "./cfg/tiny-yolo-voc-liquor.cfg"
        
    # Sets prediction threshold
    if settings.thresh != None:
        thresh = settings.thresh
    else:
        thresh = 0.5
    
    # Create directory to store the processed panoramic images
    if settings.save_dir != None:
        save_dir = settings.save_dir
    else:
        save_dir = './predictions/'
    mkdir(save_dir)
    
    # Create directory to store text files for 
    # images that were predicted to contain a 
    # store sign and those that are predicted 
    # not to have
    mkdir(join(save_dir, './predict_info/'))

    # Feed list of image paths, .cfg file, threshold, and save_dir for prediction
    # to the prediction function
    predict(image_paths, model_cfg, thresh, save_dir)                                                                
                                                                              
    print('All predictions from {} have been completed and stored in {}.'.format(settings.data_dir, save_dir))
    