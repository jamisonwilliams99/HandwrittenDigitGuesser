import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras


model = keras.models.load_model("model.h5")

data = keras.datasets.mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

train_images = train_images/255.0
test_images = test_images/255.0

#print(train_images[0])

#prediction = model.predict([train_images[0]])
#print(prediction)

single_test = train_images[78]
single_test = single_test.reshape(1, 28, 28)
print(single_test.shape)
#plt.imshow(train_images[78], cmap="gray")
#plt.show()
prediction = model.predict(single_test)
print(np.argmax(prediction))

print(single_test)

