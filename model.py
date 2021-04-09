import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras


data = keras.datasets.mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

train_images = train_images/255.0
test_images = test_images/255.0

# Sequential creates a sequence of layers where each layer is defined in order
# Flatten function "squishes" multidimensional lists into one list
# Dense layer is a fully connected layer ie each nueron is connected to every nueron in the next layer
# softmax will pick a probability at each output nueron where all of the probabillities add up to one
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(train_images, train_labels, epochs=5)

test_loss, test_acc = model.evaluate(test_images, test_labels)

print("Test Acc: ", test_acc)
model.save("model.h5")

