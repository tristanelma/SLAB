# SLAB

Download the [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) and place the unzipped folder in this repo. I've added it to my filepath but placed it in the .gitignore as it's not our work.


Move the TextRecognitionDataGenerator/TextRecognitionDataGenerator/dicts/ and TextRecognitionDataGenerator/TextRecognitionDataGenerator/fonts/ folders to the same parent folder as shown above.

Use python generation.py [keyword] to generate a 10/90 training set with that specific word. The training set will be saved in a data_generation folder with two sub-folders, positive_samples and negative_samples. These folders are also not being tracked by github.