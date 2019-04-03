# SLAB

## Step 1
- Download the [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) and place the unzipped folder in this repo (inside `CNN/`). I've added it to my filepath but placed it in the .gitignore as it's not our work.

## Step 2
- Move the `TextRecognitionDataGenerator/TextRecognitionDataGenerator/dicts/` and `TextRecognitionDataGenerator/TextRecognitionDataGenerator/fonts/` folders to the same parent folder as shown above.

## Step 3
- Enter `CNN/` and run `python detection_generation.py [keyword]` to generate a detection training set with that specific word. As of now, the training set will be 10,000 images strong. This can be edited via `detection_generation.py`. The training set will be saved in `data_generation/pictures` and the corresponding xml files will be stored in `data_generation/labels`. This data is not tracked by github.

## Step 4
1. We are using the [Yolo](https://pjreddie.com/media/files/papers/yolo.pdf) algorithm for the detection of shop signs.
2. Follow this tutorial to [install](https://keponk.wordpress.com/2017/12/07/siraj-darkflow/) OR `python3 setup.py build_ext --inplace`
3. Download ckpt folder and place it into `./darkflow` from [here](https://www.dropbox.com/s/wj55e21c1rt840d/ckpt.zip?dl=1)
4. Download build_graph folder and place it into `./darkflow` from [here](https://www.dropbox.com/s/3aoclc827ylp06r/built_graph.zip?dl=1)
5. Download bin folder and place it into `./darkflow` from [here](https://www.dropbox.com/s/3aprlyhg7fsrh4z/bin.zip?dl=1)

### Training with Pre-trained Pascal VOC weights:
*The steps below assume we want to use tiny YOLO and our dataset has 3 classes*

1. Create a copy of the configuration file `tiny-yolo-voc.cfg` and rename it according to your preference `tiny-yolo-voc-3c.cfg` (It is crucial that you leave the original `tiny-yolo-voc.cfg` file unchanged, see below for explanation).

2. In `tiny-yolo-voc-3c.cfg`, change classes in the [region] layer (the last layer) to the number of classes you are going to train for. In our case, classes are set to 3.
    
    ```python
    ...

    [region]
    anchors = 1.08,1.19,  3.42,4.41,  6.63,11.38,  9.42,5.11,  16.62,10.52
    bias_match=1
    classes=3
    coords=4
    num=5
    softmax=1
    
    ...
    ```

3. In `tiny-yolo-voc-3c.cfg`, change filters in the [convolutional] layer (the second to last layer) to num * (classes + 5). In our case, num is 5 and classes are 3 so 5 * (3 + 5) = 40 therefore filters are set to 40.
    
    ```python
    ...

    [convolutional]
    size=1
    stride=1
    pad=1
    filters=40
    activation=linear

    [region]
    anchors = 1.08,1.19,  3.42,4.41,  6.63,11.38,  9.42,5.11,  16.62,10.52
    
    ...
    ```

4. Change `labels.txt` to include the label(s) you want to train on (number of labels should be the same as the number of classes you set in `tiny-yolo-voc-3c.cfg` file). In our case, `labels.txt` will contain 3 labels.

    ```
    label1
    label2
    label3
    ```
5. Reference the `tiny-yolo-voc-3c.cfg` model when you train.

    `flow --model cfg/tiny-yolo-voc-3c.cfg --load bin/tiny-yolo-voc.weights --train --annotation train/Annotations --dataset train/Images`


* Why should I leave the original `tiny-yolo-voc.cfg` file unchanged?
    
    When darkflow sees you are loading `tiny-yolo-voc.weights` it will look for `tiny-yolo-voc.cfg` in your cfg/ folder and compare that configuration file to the new one you have set with `--model cfg/tiny-yolo-voc-3c.cfg`. In this case, every layer will have the same exact number of weights except for the last two, so it will load the weights into all layers up to the last two because they now contain different number of weights.

6. Run `./flow --model ./cfg/tiny-yolo-voc-<CUSTOM INPUT>.cfg --load bin/tiny-yolo-voc.weights --train --dataset <DATASET DIRECTORY> --annotation <ANNOTATIONS DIRECTORY> --gpu 1.0`

7. Run `python yolo_predict.py <DATA_DIRECTORY>` -> This will save the images with the bounding boxes to your desired save_dir or default: `./darkflow/predictions/`.
