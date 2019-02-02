# SLAB

## Step 1
- Download the [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) and place the unzipped folder in this repo (inside `CNN/`). I've added it to my filepath but placed it in the .gitignore as it's not our work.

## Step 2
- Move the `TextRecognitionDataGenerator/TextRecognitionDataGenerator/dicts/` and `TextRecognitionDataGenerator/TextRecognitionDataGenerator/fonts/` folders to the same parent folder as shown above.

## Step 3
- Enter `CNN/` and run `python generation.py [keyword]` to generate a 50/50 training set with that specific word. The training set will be saved in `data_generation/` with keyword photos saved as t.NUM.jpg and false photos saved as f.NUM.jpg. This data is also not tracked by github.

## Step 4
- Train a CNN binary classifier by running `python training.py -t <TEST_PERCENT> -e <EPOCHS> -l <LEARNING_RATE> -b <BATCH_SIZE>`. Note that all command-line options are optional, as we have hardcoded defaults for them: `python training.py` uses all defaults. We are still working to export the trained weights - for now you'll just be able to see some statistics about the resulting model.
