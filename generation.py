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

subprocess.call(['rm', '-rf', 'data_generation/false_samples'])
subprocess.call(['rm', '-rf', 'data_generation/positive_samples'])

# Jeff: For other flags you can use to generate the images from 
# TextRecognitionDataGenerator repo, cd into TextRecognitionDataGenerator/TextRecognitionDataGenerator/
# and call `python run.py -h`

# unaltered files get name format 0
subprocess.call(['python', 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py', '--output_dir', 'data_generation/positive_samples' , '-na' , '0' ,'-l', 'sp', '-c', '750', '-w', '1'])
subprocess.call(['python', 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py', '--output_dir', 'data_generation/false_samples' , '-na' , '0' ,'-l', 'sp', '-c', '6750', '-w', '1'])
# blurred files get name format 1
subprocess.call(['python', 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py', '--output_dir', 'data_generation/positive_samples', '-na', '1', '-l', 'sp', '-c', '375', '-w', '1', '-bl', '3', '-rbl', '-k', '45', '-rk'])
subprocess.call(['python', 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py', '--output_dir', 'data_generation/false_samples', '-na', '1', '-l', 'sp', '-c', '3375', '-w', '1', '-bl', '3', '-rbl', '-k', '45', '-rk'])
# manually altered files get name format 2
subprocess.call(['python', 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py', '--output_dir', 'data_generation/alter_pos', '-na', '2', '-l', 'sp', '-c', '375', '-w', '1', '-k', '45', '-rk'])
subprocess.call(['python', 'TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py', '--output_dir', 'data_generation/alter_false', '-na', '2', '-l', 'sp', '-c', '3375', '-w', '1', '-k', '45', '-rk'])

#altering positive samples
for i in range(375):
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
for x in range(3375):
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

    
        


    




