# -*- coding: utf-8 -*-
"""cnnproject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Em6sbIPwFw8Bg92tih495alqYRBhKjlf
"""

from google.colab import drive
drive.mount('/content/drive')

!cp '/content/drive/MyDrive/archive(10).zip' '/content/'

!unzip '/content/archive(10).zip'

import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

from tensorflow import keras
from keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.layers import Conv2D, MaxPooling2D

from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.preprocessing import image_dataset_from_directory

import os
import matplotlib.image as mpimg

dataset_path='/content/chest_xray'

path = '/content/chest_xray/chest_xray/train'
classes = os.listdir(path)
print(classes)

image_size =(150,150)
batch_size = 64
epochs=10

model = Sequential()

model.add(Conv2D(64, (3,3) , activation = 'relu' , input_shape= (150,150,3)))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64 , (3,3) , activation = 'relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64 , (3,3) , activation = 'relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64 , (3,3) , activation = 'relu'))
model.add(MaxPooling2D((2,2)))

model.add(Flatten())

model.add(Dense(512, activation = 'relu'))

model.add(Dense(1, activation = 'sigmoid'))

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

model.summary()

train_datagen=ImageDataGenerator(
    rescale=1./255
)
test_datagen = ImageDataGenerator(rescale=1./255)
val_datagen=ImageDataGenerator(rescale=1./255)

training_gen = train_datagen.flow_from_directory('chest_xray/train',
target_size=image_size,
                                                  batch_size=batch_size,
                                                 class_mode='binary')

testing_gen = test_datagen.flow_from_directory(
    directory='/content/chest_xray/chest_xray/test',
    batch_size=batch_size,
    target_size=image_size,
)

validation_generator = val_datagen.flow_from_directory(
    '/content/chest_xray/chest_xray/val' ,
target_size=image_size,
batch_size=batch_size,
class_mode='binary')

history = model.fit(training_gen,
          epochs=10,
          validation_data=validation_generator)

test_loss, test_acc = model.evaluate(validation_generator)
print('val Accuracy:', test_acc)

loss, accuracy = model.evaluate(testing_gen)
print('The accuracy of the model on test dataset is',
      np.round(accuracy*100))

plt.figure(figsize=(8,6))
plt.title(' Accuracy scores')
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['accuracy', 'val_accuracy'])
plt.show()

plt.figure(figsize=(8,6))
plt.title(' Loss value')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['loss', 'val_loss'])
plt.show()

test_image = tf.keras.utils.load_img(
    "/content/chest_xray/chest_xray/test/NORMAL/IM-0010-0001.jpeg",
    target_size=(256, 256))


plt.imshow(test_image)

from tensorflow.keras.preprocessing import image

def predict_image(image_path):
  img=image.load_img(image_path,target_size=image_size)
  img=image.img_to_array(img)
  img=np.expand_dims(img,axis=0)
  img/= 255.0

  prediction=model.predict(img)
  return "Normal" if prediction<0.5 else "Pneumonia"

output=predict_image("/content/chest_xray/chest_xray/test/NORMAL/IM-0010-0001.jpeg")
print(output)

test_image = tf.keras.utils.load_img(
     "/content/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_478.jpeg",
    target_size=(256, 256))


plt.imshow(test_image)

output=predict_image("/content/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_478.jpeg")
print(output)