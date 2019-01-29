#!/bin/bash

python data_generation/generation.py $1
cat TextRecognitionDataGenerator/TextRecognitionDataGenerator/dicts/sp.txt
./data_generation/generation.sh