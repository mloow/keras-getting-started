import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt
import random

seed = 123
random.seed(seed)

def get_sample_data(num):
    input_data = np.random.random_integers(low=0, high=1, size=(num, 2))
    output_data = [int(any(x)) for x in input_data]
    return input_data, output_data

model = Sequential()

model.add(Dense(units=1, activation='linear', input_dim=2))

model.compile(loss='mean_squared_error',
              optimizer='sgd',
              metrics=['accuracy'])

x_train, y_train = get_sample_data(100)
x_test, y_test = get_sample_data(50)

loss_stop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.001, patience=10, verbose=0, mode='auto')


history = model.fit(x_train, y_train, epochs=1000, batch_size=10, callbacks=[loss_stop])
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