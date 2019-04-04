# General Utilities
import re
import os
import sys
import random
import subprocess
from PIL import Image
from PIL import ImageDraw
import argparse
from tqdm import tqdm
from os import listdir
from os.path import isfile, join

# ML / Deep learning Utilities
import cv2
import numpy as np
from numpy import loadtxt
import pandas as pd

# Helper function to create a new folder
def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
        else:
            print("(%s) already exists" % (path))

def sliding_window(image, step_size=300, window_size=(600, 600)):
    '''
        FUNCTION: To create generator of coordinates
                  for small image of window sizes with stride and stepSize

        Parameters
        ----------
        image: (numpy.ndarray) Original image to create subset of images from
        step_size: (int) Number of Pixels to slide over when getting new image
        window_size: ((int, int)) Size (Height, Width) of derived images created

        Returns
        -------
        Python Generator of images derived from original image
    '''
    # slide a window across the image
    for x in range(0, image.shape[1] - window_size[1], step_size):
        for y in range(0, image.shape[0] - window_size[0], step_size):
            yield (x, y, x + window_size[1], y + window_size[0])

# Main function
if __name__ == '__main__':

    # Read in arguments from command line
    parser = argparse.ArgumentParser(
        description='Generates 600 x 600 sized images derived from original panoramic image.'
    )
    parser.add_argument('data_dir', metavar='DATA-DIRECTORY', action='store', help='Path to the data directory with panoramic images to be used for generating smaller images.')
    parser.add_argument('--save_dir', metavar='SAVE-DIRECTORY', action='store', help='Set directory to save all the smaller images derived from the processed panoramic image.')
    settings = parser.parse_args()

    # Store all the image names into list
    image_names = [f for f in listdir(settings.data_dir) if isfile(join(settings.data_dir, f))]

    # print(image_names)

    # Create directory to store the processed panoramic images
    if settings.save_dir != None:
        save_dir = settings.save_dir
    else:
        save_dir = './processed_panos/'
    mkdir(save_dir)

    # Loop through all the image names to create the
    # smaller images from that directory of panoramic images
    for image_name in image_names:

        img = cv2.imread(join(settings.data_dir, image_name))

        pano = Image.open(join(settings.data_dir, image_name))

        # Loop through each sliding window created
        for idx, window in tqdm(enumerate(sliding_window(img, 300, (600, 600)))):
            pano.crop(window).save(join(save_dir, '{}_{}.jpg'.format(image_name[:-4], idx)))


    print('All panoramic images in {} have been processed.'.format(settings.data_dir))
