import os
import numpy as np
import random
from keras.utils import load_img, img_to_array, to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Dropout, Flatten
from keras.losses import categorical_crossentropy
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

Plant_mapping = {
    'Amaranth': 0,
    'Apple': 1,
    'Cabbage': 2,
    'Crown_daisy': 3,
    'Cucumber': 4,
    'Lettuce': 5,
    'Orange': 6,
    'Spring_onion': 7,
    'Tomato': 8,
    'Water_spinach': 9
}

# Data for train
folder = '/content/drive/MyDrive/D/Train'
photos_train_raw, labels_train_raw = list(), list()
img_train_per_label = 220

for sub_folder in os.listdir(folder):
    sub_folder_path = os.path.join(folder, sub_folder)
    file_list = os.listdir(sub_folder_path)
    random.shuffle(file_list)

    count = 0
    for file_name in file_list:
        if count >= img_train_per_label:
            break

        output = Plant_mapping.get(sub_folder, None)

        if output is not None:
            img = load_img(os.path.join(sub_folder_path, file_name), target_size=(32, 32, 3))
            img = img_to_array(img)
            photos_train_raw.append(img)
            labels_train_raw.append(output)

            count += 1
    if len(photos_train_raw) >= img_train_per_label * 10:
        break

# Random img
indices = list(range(len(photos_train_raw)))
random.shuffle(indices)
photos_train = [photos_train_raw[i] for i in indices]
labels_train = [labels_train_raw[i] for i in indices]

photos_train = np.array(photos_train)
labels_train = np.array(labels_train)

# Data for test
folder = '/content/drive/MyDrive/D/Test'
photos_test_raw, labels_test_raw = list(), list()
img_test_per_label = 40

for sub_folder in os.listdir(folder):
    sub_folder_path = os.path.join(folder, sub_folder)
    file_list = os.listdir(sub_folder_path)
    random.shuffle(file_list)

    count = 0
    for file_name in file_list:
        if count >= img_test_per_label:
            break

        output = Plant_mapping.get(sub_folder, None)

        if output is not None:
            img = load_img(os.path.join(sub_folder_path, file_name), target_size=(32, 32, 3))
            img = img_to_array(img)
            photos_test_raw.append(img)
            labels_test_raw.append(output)

            count += 1
    if len(photos_test_raw) >= img_test_per_label * 10:
        break

# Random img
indices = list(range(len(photos_test_raw)))
random.shuffle(indices)
photos_test = [photos_test_raw[i] for i in indices]
labels_test = [labels_test_raw[i] for i in indices]

photos_test = np.array(photos_test)
labels_test = np.array(labels_test)

print(photos_train.shape)
print(labels_train.shape)
print(photos_test.shape)
print(labels_test.shape)

photos_train = photos_train.astype('float32')/255
photos_test = photos_test.astype('float32')/255

labels_train = to_categorical(labels_train, 10)
labels_test = to_categorical(labels_test, 10)

model = Sequential()

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(32, 32, 3)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(MaxPool2D((2, 2), padding='same'))
model.add(Dropout(0.25))

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(MaxPool2D((2, 2), padding='same'))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.summary()

model.compile(loss=categorical_crossentropy, optimizer='adam', metrics=['accuracy'])
model_history = model.fit(photos_train, labels_train, batch_size=64, epochs=50, steps_per_epoch=30, verbose=1, validation_data=(photos_test, labels_test), shuffle=1)

plt.figure(1, figsize=(10, 8))
plt.plot(model_history.history['accuracy'], color='green')
plt.plot(model_history.history['val_accuracy'], color='red')
plt.title('Accuracy of model')

plt.legend(['Accuracy', 'Val_Accuracy'], loc='lower right')
plt.show()

plt.figure(1, figsize=(10, 8))
plt.plot(model_history.history['loss'], color='green')
plt.plot(model_history.history['val_loss'], color='red')

plt.title('Loss of model')
plt.legend(['Loss', 'Val_Loss'], loc='upper right')
plt.show()

test_loss, test_acc = model.evaluate(photos_test, labels_test)
print(test_acc, test_loss)

model.save("/content/drive/MyDrive/A.I/CNN_AI.h5")