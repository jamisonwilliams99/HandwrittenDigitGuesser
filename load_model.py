import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras


model = keras.models.load_model("images/one_hidden_layer/model.h5")

data = keras.datasets.mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

train_images = train_images/255.0
test_images = test_images/255.0

test_index = 87

for i in range(100):
    single_test = test_images[i]
    single_test = single_test.reshape(1, 28, 28)

    plt.imshow(test_images[i], cmap="gray")
    plt.show()

    prediction = model.predict(single_test)
    print(np.argmax(prediction))



