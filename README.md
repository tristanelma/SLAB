# SLAB

## Step 1
- Download the [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) and place the unzipped folder in this repo (inside `CNN/`). I've added it to my filepath but placed it in the .gitignore as it's not our work.

## Step 2
- Move the `TextRecognitionDataGenerator/TextRecognitionDataGenerator/dicts/` and `TextRecognitionDataGenerator/TextRecognitionDataGenerator/fonts/` folders to the same parent folder as shown above.

## Step 3
- Enter `CNN/` and run `python detection_generation.py [keyword]` to generate a detection training set with that specific word. As of now, the training set will be 10,000 images strong. This can be edited via `detection_generation.py`. The training set will be saved in `data_generation/pictures` and the corresponding xml files will be stored in `data_generation/labels`. This data is not tracked by github.

## Step 4
- We are using the [Yolo](https://pjreddie.com/media/files/papers/yolo.pdf) algorithm for the detection of shop signs.

### Yolo intuition:
1. Split the image into a grid 
2. Each grid cell is now responsible for creating 
