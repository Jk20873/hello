
!pip install tensorflow==1.3.0
!pip install keras==2.0.7



import numpy as np
import os
import time
from CE888_2021.Lab_8.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.layers import Dense, Activation, Flatten
from keras.layers import merge, Input
from keras.models import Model
from keras.utils import np_utils
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

# Upload data
from zipfile import ZipFile
file_name = "/content/CE888_2021/Lab_8/data.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('done')


file_name = "/content/train.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('done')

"""**Creating specific directories for training, evaluation and testing. Moving the corresponding data to these directories.**"""

original_dataset_dir = '/content/train'
base_dir = '/content/cats_and_dogs'

os.mkdir(base_dir)

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')
train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')
validation_cats_dir = os.path.join(validation_dir, 'cats')
validation_dogs_dir = os.path.join(validation_dir, 'dogs')
test_cats_dir = os.path.join(test_dir, 'cats')
test_dogs_dir = os.path.join(test_dir, 'dogs')

os.mkdir(train_dir)
os.mkdir(validation_dir)
os.mkdir(test_dir)
os.mkdir(train_cats_dir)
os.mkdir(train_dogs_dir)
os.mkdir(validation_cats_dir)
os.mkdir(validation_dogs_dir)
os.mkdir(test_cats_dir)
os.mkdir(test_dogs_dir)

import shutil
fnames = ['cat.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_cats_dir, fname)
    #print(src,dst)
    shutil.copyfile(src, dst)
    
fnames = ['cat.{}.jpg'.format(i) for i in range(1000, 1500)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_cats_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['cat.{}.jpg'.format(i) for i in range(1500, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_cats_dir, fname)
    shutil.copyfile(src, dst)
    
fnames = ['dog.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_dogs_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['dog.{}.jpg'.format(i) for i in range(1000, 1500)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_dogs_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['dog.{}.jpg'.format(i) for i in range(1500, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_dogs_dir, fname)
    shutil.copyfile(src, dst)

print('total training cat images:', len(os.listdir(train_cats_dir)))
print('total training dog images:', len(os.listdir(train_dogs_dir)))
print('total validation cat images:', len(os.listdir(validation_cats_dir)))

print('total validation dog images:', len(os.listdir(validation_dogs_dir)))
print('total test cat images:', len(os.listdir(test_cats_dir)))
print('total test dog images:', len(os.listdir(test_dogs_dir)))

"""**Pre-processing the images from each of the created directories and storing them in numpy arrays (in-memory).**"""

train_dir_list = os.listdir(train_dir)
validation_dir_list = os.listdir(validation_dir)
test_dir_list = os.listdir(test_dir)

def create_image_list(data_dir_list, data_dir):
  img_data_list = []
  for dataset in data_dir_list:
    img_list = os.listdir(data_dir + '/' + dataset)
    print ('Loading the images of dataset-'+'{}\n'.format(dataset))
    for img in img_list:
      img_path = data_dir + '/'+ dataset + '/'+ img
      img = image.load_img(img_path, target_size=(224, 224))
      x = image.img_to_array(img)
      x = np.expand_dims(x, axis=0)
      x = preprocess_input(x)
      img_data_list.append(x)
  return img_data_list

train_images = np.array(create_image_list(train_dir_list, train_dir))
print(train_images.shape)
train_images = np.rollaxis(train_images, 1, 0)
print (train_images.shape)
train_images = train_images[0]
print (train_images.shape)

validation_images = np.array(create_image_list(validation_dir_list, validation_dir))
print(validation_images.shape)
validation_images = np.rollaxis(validation_images, 1, 0)
print (validation_images.shape)
validation_images = validation_images[0]
print (validation_images.shape)

test_images = np.array(create_image_list(test_dir_list, test_dir))
print(test_images.shape)
test_images = np.rollaxis(test_images, 1, 0)
print (test_images.shape)
test_images = test_images[0]
print (test_images.shape)

"""**Creating the corresponding classification labels for each numpy array.**"""

num_classes = 2
label_names = ['dogs', 'cats']

train_num_samples = train_images.shape[0]
train_labels = np.ones((train_num_samples,), dtype='int64')
train_labels[0 : int(train_num_samples / 2)] = 0
train_labels[int(train_num_samples / 2) :] = 1
train_labels = np_utils.to_categorical(train_labels, num_classes)

validation_num_samples = validation_images.shape[0]
validation_labels = np.ones((validation_num_samples,), dtype='int64')
validation_labels[0 : int(validation_num_samples / 2)] = 0
validation_labels[int(validation_num_samples / 2) :] = 1
validation_labels = np_utils.to_categorical(validation_labels, num_classes)

test_num_samples = test_images.shape[0]
test_labels = np.ones((test_num_samples,), dtype='int64')
test_labels[0 : int(test_num_samples / 2)] = 0
test_labels[int(test_num_samples / 2) :] = 1
test_labels = np_utils.to_categorical(test_labels, num_classes)

"""**Importing the model and replacing the last layer for achieving transfer learning.**"""

image_input = Input(shape=(224, 224, 3)) # shape of a single image
model = VGG16(input_tensor=image_input, include_top=True, weights='imagenet') # load VGG-16 model with 'top = true'
model.summary()

last_layer = model.get_layer('fc2').output
out = Dense(num_classes, activation='softmax', name='output')(last_layer)
custom_vgg_model = Model(image_input, out)
custom_vgg_model.summary()

for layer in custom_vgg_model.layers[:-1]:
	layer.trainable = False

custom_vgg_model.summary()
custom_vgg_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

"""**Training the modified model.**"""

t = time.time()
hist = custom_vgg_model.fit(train_images, train_labels, batch_size=6, epochs=2, verbose=1, validation_data=(validation_images, validation_labels))
print('Training time: %s' % (time.time() - t))
(loss, accuracy) = custom_vgg_model.evaluate(test_images, test_labels, batch_size=10, verbose=1)

print()
print(f"Test results on {len(test_images)}")
print("loss={:.4f}, accuracy: {:.4f}%".format(loss, accuracy * 100))

"""**Plotting the train loss and accuracy against the validation loss and accuracy.**"""

import matplotlib.pyplot as plt

# visualizing losses and accuracy
train_loss=hist.history['loss']
val_loss=hist.history['val_loss']
train_acc=hist.history['acc']
val_acc=hist.history['val_acc']
xc=range(2)

plt.figure(1,figsize=(7,5))
plt.plot(xc,train_loss)
plt.plot(xc,val_loss)
plt.xlabel('num of Epochs')
plt.ylabel('loss')
plt.title('train_loss vs val_loss')
plt.grid(True)
plt.legend(['train','val'])
plt.style.use(['classic'])

plt.figure(2,figsize=(7,5))
plt.plot(xc,train_acc)
plt.plot(xc,val_acc)
plt.xlabel('num of Epochs')
plt.ylabel('accuracy')
plt.title('train_acc vs val_acc')
plt.grid(True)
plt.legend(['train','val'],loc=4)
plt.style.use(['classic'])
