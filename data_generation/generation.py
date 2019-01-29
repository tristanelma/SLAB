import sys
import random

sample_word = sys.argv[1]

lang = open('dicts/sp.txt','w') 
lang.write(sample_word + '\n')
lang.close()

shell = open('data_generation/generation.sh', 'w')
shell.write('python TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py --output_dir data_generation/positive_samples -l sp -c 750 -w 1 -bl 3 -rbl -k 45 -rk\n')
shell.write('python TextRecognitionDataGenerator/TextRecognitionDataGenerator/run.py --output_dir data_generation/false_samples -l en -c 6750 -w 1 -bl 3 -rbl -k 45 -rk\n')
print("File created")
shell.close()
    
        


    




