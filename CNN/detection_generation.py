import cv2
import math
import os
from random import randint
import random
import sys
import numpy as np
from scipy.ndimage import imread
from coordinates_to_xml import write_xml

from PIL import Image, ImageDraw, ImageFilter, ImageOps

def rand_back(back_dir):
    a=random.choice(os.listdir(back_dir))
    file = back_dir+a
    return Image.open(file)

def assembled_background_photo(special_word, height, width, pic_file, xml_file, picture_dir, back_dir):
    back_image = rand_back(back_dir)

    # word we care about
    im_1 = Image.open(special_word)
    # make image black and white
    im_1 = im_1.convert('L')
    if (random.uniform(0,1) > 0.5):
        im_1 = ImageOps.invert(im_1)
    angle = random.randint(-3,3)
    rot = im_1.rotate(angle, expand=1)
    r_w, r_h = rot.size
    x = (randint(0, max(1,width-r_w)))
    y = (randint(0, max(1,height-r_h)))
    position = (x, y)
    back_image.paste(rot, position, rot)
    if (random.uniform(0,1) > 0.7):
        w = random.randint(1, back_image.size[1]/4)
        x1 = random.randint(0, back_image.size[0])
        y1 = random.randint(0, back_image.size[1])
        x2 = random.randint(0, back_image.size[0])
        y2 = random.randint(0, back_image.size[1])
        img_draw = ImageDraw.Draw(back_image)
        img_draw.line([(x1, y1), (x2, y2)], width=w, fill='brown')
    
    back_image = back_image.convert('L')
    #saving relevant xml file
    write_xml(xml_file, 'sign' , x, x+r_w, y, y+r_h, width, height, pic_file)

    back_image.save(processed_photos + pic_file)

if __name__ == '__main__':
    sample_word = "liquor"

    languages = ['en', 'es', 'cn', 'de', 'fr']

    # sample_word = sys.argv[1]
    DATA_PATH_1 = 'data_generation/specialword/'
    DATA_PATH_2 = 'data_generation/randomwords/'
    processed_photos = 'data_generation/pictures/'
    labels = 'data_generation/labels/'
    BACKGROUND_DIR = 'background_images/'


    lang = open('dicts/sp.txt','w') 
    lang.write(sample_word + '\n')
    lang.close()

    POSITIVE_SAMPLES = 2000
    SAMPLES_PER_LANGUAGE = 2000/5
    HEIGHT = 600
    WIDTH = 600

    DATAGEN_LOC = 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py'
    os.system('rm -rf ' + labels)
    os.system('rm -rf ' + processed_photos)
    os.system('rm -rf ' + DATA_PATH_1)
    os.system('rm -rf ' + DATA_PATH_2)


    for i in range(POSITIVE_SAMPLES):
        os.system('python ' + DATAGEN_LOC + ' --output_dir data_generation/specialword -na 0 -l sp -c ' + str(int(POSITIVE_SAMPLES/2)) + ' -w 2 -b')
        os.system('python ' + DATAGEN_LOC + ' --output_dir data_generation/specialword -na 0 -l sp -c ' + str(int(POSITIVE_SAMPLES/2)) + ' -w 2 -bl 2 -rbl -b')
    # iterate through languages
    for i in range(len(languages)):
        language = languages[i]
        os.system('python ' + DATAGEN_LOC + ' --output_dir data_generation/randomwords -na 0 -l ' + language + ' -c ' + str(int(SAMPLES_PER_LANGUAGE/2)) + ' -w 2 -b')
        os.system('python ' + DATAGEN_LOC + ' --output_dir data_generation/randomwords -na 0 -l ' + language + ' -c ' + str(int(SAMPLES_PER_LANGUAGE/2)) + ' -w 2 -bl 2 -rbl -b')
    # os.system('python ' + DATAGEN_LOC + ' --output_dir data_generation/randomwords -na 0 -l en -c ' + str(2*POSITIVE_SAMPLES) + ' -w 1')

    #image = np.ones((HEIGHT, WIDTH)) * 255
    #cv2.randn(image, 235, 10)
    #back_image = Image.fromarray(image).convert('RGB')

    special_files = os.listdir(DATA_PATH_1)
    ran_files = os.listdir(DATA_PATH_2)
    list_of_special = []
    list_of_ran = []    
    for _, input_file in enumerate(special_files):
        list_of_special.append(DATA_PATH_1 + input_file)
    for _, input_file in enumerate(ran_files):
        list_of_ran.append(DATA_PATH_2 + input_file)
    
    i = 0
    os.system('mkdir data_generation/pictures/')
    os.system('mkdir data_generation/labels/')
    while(i < len(list_of_special)):
        special_word = list_of_special[i]
        rand_word = list_of_ran[i]

        assembled_background_photo(special_word, HEIGHT, WIDTH, 'positive' + str(i) + '.jpg', labels + 'positive' + str(i) + '.xml', processed_photos, BACKGROUND_DIR)
        i += 1
    
    # os.system('rm -rf ' + DATA_PATH_1)
    # os.system('rm -rf ' + DATA_PATH_2)
    
