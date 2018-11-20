from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
import matplotlib.pyplot as plt

from time import time
import os, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Hide messy TensorFlow warnings
warnings.filterwarnings("ignore") # Hide messy Numpy warnings

# load the data
features = np.load('x_data.npy')
targets = np.load('y_data.npy')

# define three standard deviations
std = 3

# get the outliers indices
outliers_indices = [i for i in range(len(targets)) if (abs(targets[i] - np.mean(targets)) > std*np.std(targets))]

# delete them
features = np.delete(features, outliers_indices, axis=0)
targets = np.delete(targets, outliers_indices)

# split the data 20% samples on test
features_train, features_test, targets_train, targets_test = train_test_split(features, targets, test_size=0.20)

# hyperparameters
seq_len = 10
params = 5
epochs = 100
batch_size = 512
units = 50
patience = 3

# build the model
model = Sequential()
model.add(LSTM(input_shape=(seq_len, params), output_dim=units, return_sequences=True, activation='relu'))
model.add(LSTM(units, return_sequences=False, activation='relu'))
model.add(Dense(units, kernel_initializer='lecun_uniform', activation='relu'))
model.add(Dense(1, kernel_initializer='lecun_uniform', activation='linear'))
model.compile(optimizer='adam',loss='mae', metrics=['mse','mae','mape','cosine'])
model.summary()

# declare the callbacks
callbacks = [
    EarlyStopping(monitor='mae', patience=patience),
    ModelCheckpoint(filepath='best_model.h5', monitor='mae', save_best_only=True),
    TensorBoard(log_dir="logs/{}".format(time()))]

# train
history = model.fit(features_train, targets_train, epochs=epochs, callbacks=callbacks, verbose=1, batch_size=batch_size, validation_data=(features_test, targets_test))

# history
#
# predicted = model.predict(features_test)
# predicted = np.reshape(predicted, (predicted.size,))
# predicted
#
# gg = pd.DataFrame(targets_test - predicted)
# gg.mean()
# gg.hist(alpha=0.8, bins=100)
# plt.show()
#
# model.save("model")
#
# import pandas as pd
# import matplotlib.pyplot as plt
# df_targets = pd.DataFrame(targets)
# df_targets.mean()
# df_targets.plot(figsize=(200,5))
# plt.show()
