import numpy as np
from keras.datasets import mnist
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.utils import np_utils

class Model:
	def __init__(self):
		# Load trained neural network model
		self.mnist_model = load_model('keras_mnist.h5')

	def predict_number(self,img):
		# reshape img to fit model
		img = img.reshape(1,784)
		img = img.astype('float32')
		img /= 255

		pred = self.mnist_model.predict(img)
		pred = np.argmax(pred, axis=1)

		return pred[0]