import sys
import random
import subprocess
import os
from scipy.ndimage import imread
from scipy.misc import imsave
import cv2

from PIL import Image
from PIL import ImageDraw

sample_word = sys.argv[1]

lang = open('dicts/sp.txt','w') 
lang.write(sample_word + '\n')
lang.close()

# to do: add random color in text generation, random line generation
total_size = 20000
positive_split = 0.5
negative_split = 0.5
training_split = 0.8
test_split = 0.2
unaltered_split = 0.5
blurred_split = 0.25
drawn_split = 0.25
RESIZE_WIDTH=32
RESIZE_HEIGHT=32
DATA_PATH_1 = 'data_generation/positive_samples/'
DATA_PATH_2 = 'data_generation/false_samples/'

subprocess.call(['rm', '-rf', 'data_generation'])
subprocess.call(['mkdir', 'data_generation'])
subprocess.call(['rm', '-rf', 'data_generation/positive_samples'])
subprocess.call(['rm', '-rf', 'data_generation/false_samples'])

# Path to textrecognitiondatagenerator
DATAGEN_LOC = 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py'

#training
# unaltered files get name format 0
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/positive_samples' , '-na' , '0' ,'-l', 'sp', '-c', str(int(total_size*positive_split*unaltered_split)), '-w', '1'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/false_samples' , '-na' , '0' ,'-l', 'en', '-c', str(int(total_size*negative_split*unaltered_split)), '-w', '1'])
# blurred files get name format 1
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/positive_samples', '-na', '1', '-l', 'sp', '-c', str(int(total_size*positive_split*blurred_split)), '-w', '1', '-bl', '2', '-rbl', '-k', '45', '-rk'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/false_samples', '-na', '1', '-l', 'en', '-c', str(int(total_size*negative_split*blurred_split)), '-w', '1', '-bl', '2', '-rbl', '-k', '45', '-rk'])
# manually altered files get name format 2
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/alter_pos', '-na', '2', '-l', 'sp', '-c', str(int(total_size*positive_split*drawn_split)), '-w', '1', '-k', '45', '-rk'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/alter_false', '-na', '2', '-l', 'en', '-c', str(int(total_size*negative_split*drawn_split)), '-w', '1', '-k', '45', '-rk'])

#altering positive samples
for i in range(int(total_size*positive_split*drawn_split)):
    img = Image.open('data_generation/alter_pos/%d.jpg' % i)
    w = random.randint(1, img.size[1]/2)
    x1 = random.randint(0, img.size[0])
    y1 = random.randint(0, img.size[1])
    x2 = random.randint(0, img.size[0])
    y2 = random.randint(0, img.size[1])
    img_draw = ImageDraw.Draw(img)
    img_draw.line([(x1, y1), (x2, y2)], width=w, fill='brown')
    img.save('data_generation/positive_samples/%d.jpg' % i)

#altering false samples
for x in range(int(total_size*negative_split*drawn_split)):
    img = Image.open('data_generation/alter_false/%d.jpg' % x)
    w = random.randint(1, img.size[1]/2)
    x1 = random.randint(0, img.size[0])
    y1 = random.randint(0, img.size[1])
    x2 = random.randint(0, img.size[0])
    y2 = random.randint(0, img.size[1])
    img_draw = ImageDraw.Draw(img)
    img_draw.line([(x1, y1), (x2, y2)], width=w, fill='brown')
    img.save('data_generation/false_samples/%d.jpg' % x)

subprocess.call(['rm', '-rf', 'data_generation/alter_false'])
subprocess.call(['rm', '-rf', 'data_generation/alter_pos'])

files_1 = os.listdir(DATA_PATH_1)
for i, input_file in enumerate(files_1):
    img = imread(DATA_PATH_1 + input_file)
    img = cv2.resize(img, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_CUBIC)
    imsave('data_generation/t.' + str(i) + '.jpg', img)

files_2 = os.listdir(DATA_PATH_2)
for i, input_file in enumerate(files_2):
    img = imread(DATA_PATH_2 + input_file)
    img = cv2.resize(img, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_CUBIC)
    imsave('data_generation/f.' + str(i) + '.jpg', img)
    
subprocess.call(['rm', '-rf', 'data_generation/positive_samples'])
subprocess.call(['rm', '-rf', 'data_generation/false_samples'])
    




