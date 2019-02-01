import sys
import random
import subprocess

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

subprocess.call(['rm', '-rf', 'data_generation/training'])
subprocess.call(['rm', '-rf', 'data_generation/testing'])

# Path to textrecognitiondatagenerator
DATAGEN_LOC = 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py'

#training
# unaltered files get name format 0
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/training/positive_samples' , '-na' , '0' ,'-l', 'sp', '-c', str(int(total_size*positive_split*training_split*unaltered_split)), '-w', '1'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/training/false_samples' , '-na' , '0' ,'-l', 'en', '-c', str(int(total_size*negative_split*training_split*unaltered_split)), '-w', '1'])
# blurred files get name format 1
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/training/positive_samples', '-na', '1', '-l', 'sp', '-c', str(int(total_size*positive_split*training_split*blurred_split)), '-w', '1', '-bl', '3', '-rbl', '-k', '45', '-rk'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/training/false_samples', '-na', '1', '-l', 'en', '-c', str(int(total_size*negative_split*training_split*blurred_split)), '-w', '1', '-bl', '3', '-rbl', '-k', '45', '-rk'])
# manually altered files get name format 2
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/training/alter_pos', '-na', '2', '-l', 'sp', '-c', str(int(total_size*positive_split*training_split*drawn_split)), '-w', '1', '-k', '45', '-rk'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/training/alter_false', '-na', '2', '-l', 'en', '-c', str(int(total_size*negative_split*training_split*drawn_split)), '-w', '1', '-k', '45', '-rk'])

#testing
# unaltered files get name format 0
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/testing/positive_samples' , '-na' , '0' ,'-l', 'sp', '-c',str(int(total_size*positive_split*test_split*unaltered_split)), '-w', '1'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/testing/false_samples' , '-na' , '0' ,'-l', 'en', '-c', str(int(total_size*negative_split*test_split*unaltered_split)), '-w', '1'])
# blurred files get name format 1
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/testing/positive_samples', '-na', '1', '-l', 'sp', '-c', str(int(total_size*positive_split*test_split*blurred_split)), '-w', '1', '-bl', '3', '-rbl', '-k', '45', '-rk'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/testing/false_samples', '-na', '1', '-l', 'en', '-c', str(int(total_size*negative_split*test_split*blurred_split)), '-w', '1', '-bl', '3', '-rbl', '-k', '45', '-rk'])
# manually altered files get name format 2
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/testing/alter_pos', '-na', '2', '-l', 'sp', '-c', str(int(total_size*positive_split*test_split*drawn_split)), '-w', '1', '-k', '45', '-rk'])
subprocess.call(['python', DATAGEN_LOC, '--output_dir', 'data_generation/testing/alter_false', '-na', '2', '-l', 'en', '-c', str(int(total_size*negative_split*test_split*drawn_split)), '-w', '1', '-k', '45', '-rk'])

#altering positive samples
for i in range(int(total_size*positive_split*training_split*drawn_split)):
    img = Image.open('data_generation/training/alter_pos/%d.jpg' % i)
    w = random.randint(1, img.size[1]/2)
    x1 = random.randint(0, img.size[0])
    y1 = random.randint(0, img.size[1])
    x2 = random.randint(0, img.size[0])
    y2 = random.randint(0, img.size[1])
    img_draw = ImageDraw.Draw(img)
    img_draw.line([(x1, y1), (x2, y2)], width=w, fill='brown')
    img.save('data_generation/training/positive_samples/%d.jpg' % i)

for i in range(int(total_size*positive_split*test_split*drawn_split)):
    img = Image.open('data_generation/testing/alter_pos/%d.jpg' % i)
    w = random.randint(1, img.size[1]/2)
    x1 = random.randint(0, img.size[0])
    y1 = random.randint(0, img.size[1])
    x2 = random.randint(0, img.size[0])
    y2 = random.randint(0, img.size[1])
    img_draw = ImageDraw.Draw(img)
    img_draw.line([(x1, y1), (x2, y2)], width=w, fill='brown')
    img.save('data_generation/testing/positive_samples/%d.jpg' % i)

#altering false samples
for x in range(int(total_size*negative_split*training_split*drawn_split)):
    img = Image.open('data_generation/training/alter_false/%d.jpg' % x)
    w = random.randint(1, img.size[1]/2)
    x1 = random.randint(0, img.size[0])
    y1 = random.randint(0, img.size[1])
    x2 = random.randint(0, img.size[0])
    y2 = random.randint(0, img.size[1])
    img_draw = ImageDraw.Draw(img)
    img_draw.line([(x1, y1), (x2, y2)], width=w, fill='brown')
    img.save('data_generation/training/false_samples/%d.jpg' % x)

for x in range(int(total_size*negative_split*test_split*drawn_split)):
    img = Image.open('data_generation/testing/alter_false/%d.jpg' % x)
    w = random.randint(1, img.size[1]/2)
    x1 = random.randint(0, img.size[0])
    y1 = random.randint(0, img.size[1])
    x2 = random.randint(0, img.size[0])
    y2 = random.randint(0, img.size[1])
    img_draw = ImageDraw.Draw(img)
    img_draw.line([(x1, y1), (x2, y2)], width=w, fill='brown')
    img.save('data_generation/testing/false_samples/%d.jpg' % x)

subprocess.call(['rm', '-rf', 'data_generation/training/alter_false'])
subprocess.call(['rm', '-rf', 'data_generation/training/alter_pos'])
subprocess.call(['rm', '-rf', 'data_generation/testing/alter_false'])
subprocess.call(['rm', '-rf', 'data_generation/testing/alter_pos'])
    




