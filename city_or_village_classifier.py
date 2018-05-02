import csv
import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# set random seeds
seed = int(time.time())
np.random.seed(seed)
random.seed(seed)
import tensorflow as tf
tf.set_random_seed(seed)

num_training_sampels = 448

# read the sample data from file
with open('samples.csv', encoding='utf-8', newline='') as f:
	reader = csv.reader(f, delimiter=',')
	data = [(row[0], row[1], row[2:]) for row in reader]

# split up into city and village sets
data_city = [(feature, 0) for (_, label, feature) in data if label == 'city']
data_village = [(feature, 1) for (_, label, feature) in data if label == 'village']

# shuffle sets
random.shuffle(data_city)
random.shuffle(data_village)

# define training set, 1:1 ratio between city and village samples
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

# build the model
model = Sequential()

# two hidden layers of 10 units each, "input layer" with 10 nodes (1 for each of the bins in the LBP histogram)
model.add(Dense(units=10, activation='relu', input_dim=10))
model.add(Dense(units=10, activation='relu'))

# a single unit in the output layer
model.add(Dense(units=1, activation='relu'))

# compile the model with MSE as loss, stochastic gradient descent as optimizer, and accuracy as metric
model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

# stop training when loss decreases less than 0.00001 for 20 consecutive epochs
loss_stop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.00001, patience=20, verbose=0, mode='auto')

# fit, aka train, the model, on the training set for a maximum of 5000 epochs, pass 32 samples before updating weights
history = model.fit(x_train, y_train, epochs=5000, batch_size=32, callbacks=[loss_stop])

# evaluate the model on the test set
loss_and_metrics = model.evaluate(x_test, y_test)

# print the accuracy of the model on the test set
print("Accuracy: " + str(loss_and_metrics[1]))

# plot loss and accuracy over epoch, in training
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'])
plt.xlabel('epochs')
plt.ylabel('loss')

plt.subplot(1, 2, 2)
plt.plot(history.history['acc'])
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.show()