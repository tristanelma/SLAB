# SLAB

## Step 1
- Download the [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) and place the unzipped folder in this repo (inside `CNN/`). I've added it to my filepath but placed it in the .gitignore as it's not our work.

## Step 2
- Move the `TextRecognitionDataGenerator/TextRecognitionDataGenerator/dicts/` and `TextRecognitionDataGenerator/TextRecognitionDataGenerator/fonts/` folders to the same parent folder as shown above.

## Step 3
- Enter `CNN/` and run `python generation.py [keyword]` to generate a 50/50 training set with that specific word. The training set will be saved in `data_generation/` with keyword photos saved as t.NUM.jpg and false photos saved as f.NUM.jpg. This data is also not tracked by github.