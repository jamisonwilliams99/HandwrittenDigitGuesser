import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras

data = keras.datasets.mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

train_images = train_images/255.0
test_images = test_images/255.0

# Sequential creates a sequence of layers where each layer is defined in order
# Flatten function "squishes" multidimensional array into one array
# Dense layer is a fully connected layer ie each neuron is connected to every neuron in the next layer
# softmax will pick a probability at each output neuron where all of the probabilities add up to one


model = keras.Sequential([
    # input layer - flattened
    keras.layers.Flatten(input_shape=(28, 28)),

    # hidden layers
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(128, activation="relu"),

    # output layer (0-9)
    keras.layers.Dense(10, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(train_images, train_labels, epochs=3)

test_loss, test_acc = model.evaluate(test_images, test_labels)

print("Test Acc: ", test_acc)
model.save("model2.h5")

