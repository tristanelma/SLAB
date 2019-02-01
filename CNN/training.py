# Imports, make sure you have cv2 installed!
import os
import sys
import numpy as np
from scipy.ndimage import imread
from scipy.misc import imsave
import cv2
import sklearn.utils
import subprocess

from keras.models import Sequential
from keras.layers import Input, Dropout, Flatten, Conv2D, MaxPooling2D, Dense, Activation
from keras.optimizers import RMSprop
from keras.layers.normalization import BatchNormalization
from keras.constraints import max_norm

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# You are not allowed to change any of these constants.

DATA_PATH = 'data_generation/'
TEST_PERCENT = 0.2
SELECT_SUBSET_PERCENT = 1

# The cat and dog images are of variable size.
RESIZE_WIDTH=32
RESIZE_HEIGHT=32
EPOCHS = 5
batch_size = 64

# Lets get started by loading the data.
X = []
Y = []

DISPLAY_COUNT = 1000

files = os.listdir(DATA_PATH)
shuffled_files = sklearn.utils.shuffle(files)
print('Going to load %i files' % len(shuffled_files))

for i, input_file in enumerate(shuffled_files):
    if i % DISPLAY_COUNT == 0 and i != 0:
        print('Have loaded %i samples' % i)
        
    img = imread(DATA_PATH + input_file)
    img = cv2.resize(img, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_CUBIC)
    X.append(img)
    if 't' == input_file.split('.')[0]:
        Y.append(1.0)
    else:
        Y.append(0.0)
        
X = np.array(X)
Y = np.array(Y)

test_size = int(len(X) * TEST_PERCENT)

test_X = X[:test_size]
test_Y = Y[:test_size]
train_X = X[test_size:]
train_Y = Y[test_size:]

print('Train set has dimensionality %s' % str(train_X.shape))
print('Test set has dimensionality %s' % str(test_X.shape))

# Apply some normalization here.
train_X = train_X.astype('float32')
test_X = test_X.astype('float32')
train_X /= 255
test_X /= 255

#model construction
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', kernel_initializer='glorot_normal', input_shape=(RESIZE_WIDTH, RESIZE_HEIGHT, 3)))
#model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3), padding='same', kernel_initializer='glorot_normal'))
#model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3, 3), padding='same', kernel_initializer='glorot_normal'))
#model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='glorot_normal'))
#model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

# Fully connected layer
model.add(Dense(512, kernel_initializer='glorot_normal'))
#model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1, kernel_initializer='glorot_normal'))
model.add(Activation('sigmoid'))

# Define your loss and your objective
optimizer = RMSprop(lr=1e-4)
loss = 'binary_crossentropy'
model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])


model.fit(train_X, train_Y, batch_size=batch_size, epochs=EPOCHS, validation_split=0.2, verbose=1, shuffle=True)

loss, acc = model.evaluate(test_X, test_Y, batch_size=batch_size, verbose=1)
print('')
print('Got %.2f%% accuracy' % (acc * 100.))

predictions = model.predict(test_X)
for i in range(len(predictions)):
    if predictions[i] < 0.5:
        predictions[i] = 0.0
    else:
        predictions[i] = 1.0
    
print(classification_report(test_Y, predictions))
print(confusion_matrix(test_Y, predictions))