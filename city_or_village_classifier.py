import csv
import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt
import random
import time

seed = int(time.time())
np.random.seed(seed)
random.seed(seed)
import tensorflow as tf
tf.set_random_seed(seed)

num_training_sampels = 448

data = []

# read the sample data from file
with open('samples.csv', encoding='utf-8', newline='') as f:
	reader = csv.reader(f, delimiter=',')
	for row in reader:
		data.append((row[0], row[1], row[2:]))

# split up into city and village sets
data_city = [(center, 0) for (_, label, center) in data if label == 'city']
data_village = [(center, 1) for (_, label, center) in data if label == 'village']

# shuffle sets
random.shuffle(data_city)
random.shuffle(data_village)

# define the training data by taking an equal number of samples from each set
train_city = data_city[:int(num_training_sampels/2)]
train_village = data_village[:int(num_training_sampels/2)]
train_data = train_city + train_village
random.shuffle(train_data)

# put the remaining samples in the test set
test_city = data_city[int(num_training_sampels/2):]
test_village = data_village[int(num_training_sampels/2):]
test_data = test_city + test_village
random.shuffle(test_data)

# split training and test data into features and labels
x_train = np.array([np.array(x) for (x, _) in train_data])
y_train = np.array([y for (_, y) in train_data])
x_test  = np.array([np.array(x) for (x, _) in test_data])
y_test  = np.array([y for (_, y) in test_data])

model = Sequential()
model.add(Dense(units=20, activation='relu', input_dim=10))
model.add(Dense(units=1, activation='relu'))
model.compile(loss='mean_squared_error',
              optimizer='sgd',
              metrics=['accuracy'])

loss_stop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.0001, patience=10, verbose=0, mode='auto')
history = model.fit(x_train, y_train, epochs=5000, batch_size=32, callbacks=[loss_stop])
loss_and_metrics = model.evaluate(x_test, y_test)

print("Accuracy: " + str(loss_and_metrics[1]))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'])
plt.xlabel('epochs')
plt.ylabel('loss')

plt.subplot(1, 2, 2)
plt.plot(history.history['acc'])
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.show()