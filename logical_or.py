# for neural network modelling
import keras
from keras.models import Sequential
from keras.layers import Dense

# for arrays and random sampling
import numpy as np

# for plotting
import matplotlib.pyplot as plt

# generate sample data for logical OR-gate
def get_sample_data(num):
    input_data = np.random.random_integers(low=0, high=1, size=(num, 2))
    output_data = [int(any(x)) for x in input_data]
    return input_data, output_data

# generate training sets and test sets
x_train, y_train = get_sample_data(100)
x_test, y_test = get_sample_data(50)

# instatiate the model
model = Sequential()

# add a layer (the only layer, the output layer) with one node.
# we also specify the number of inputs to this layer.
# since this is the only layer, the input dimension should correspond to the dimension of the input, i.e. 2
model.add(Dense(units=1, activation='linear', input_dim=2))

# compile the model, using MSE as loss function, stochastic gradient descent as optimizer method, and accuracy as metric
model.compile(loss='mean_squared_error',
              optimizer='sgd',
              metrics=['accuracy'])

# define a early-stopping callback, which will halt the training when the loss function has not improved more than 0.001 for 10 consecutive epochs
loss_stop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.001, patience=10, verbose=0, mode='auto')

# fit the model to the training set, update weights after 10 samples, train for a maximum of 1000 epochs
history = model.fit(x_train, y_train, epochs=1000, batch_size=10, callbacks=[loss_stop])

# evaluate the model on the test set
loss_and_metrics = model.evaluate(x_test, y_test)

# print the accuracy -- the permance -- of the model when used on the test set
print("Accuracy: " + str(loss_and_metrics[1]))

# plot loss and accuracy vs epochs from the training
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'])
plt.xlabel('epochs')
plt.ylabel('loss')

plt.subplot(1, 2, 2)
plt.plot(history.history['acc'])
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.show()
