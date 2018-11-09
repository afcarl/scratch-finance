from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

from time import time
import os, warnings
import numpy as np
from sklearn.cross_validation import train_test_split

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Hide messy TensorFlow warnings
warnings.filterwarnings("ignore") # Hide messy Numpy warnings

# load the data
features = np.load('x_data.npy')
targets = np.load('y_data.npy')

# split the data 20% samples on test
features_train, features_test, targets_train, targets_test = train_test_split(features, targets, test_size=0.20)

# hyperparameters
seq_len = 10
params = 5
epochs = 100
batch_size = 512
units = 10
patience = 2

# build the model
model = Sequential()
model.add(LSTM(input_shape=(seq_len, params), output_dim=units, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units, kernel_initializer='lecun_uniform', activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, kernel_initializer='lecun_uniform', activation='linear'))
model.add(Activation("linear"))
model.compile(optimizer='adam',loss='mean_squared_error')
model.summary()

# declare the callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=patience),
    ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True),
    TensorBoard(log_dir="logs/{}".format(time()))]

# train
history = model.fit(features_train, targets_train, epochs=epochs, callbacks=callbacks, verbose=1, batch_size=batch_size, validation_data=(features_test, targets_test))

# history
#
# predicted = model.predict(features_test)
# predicted = np.reshape(predicted, (predicted.size,))
# predicted
#
# import pandas as pd
# import matplotlib.pyplot as plt
# df_targets = pd.DataFrame(targets)
# df_targets.mean()
# df_targets.plot(figsize=(200,5))
# plt.show()
