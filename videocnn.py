import tensorflow as tf
from tensorflow.keras import layers, models

# Parameters
frame_count = 60  # Number of frames per video
frame_height = 64  # Frame height
frame_width = 64  # Frame width
channels = 3  # RGB channels
num_classes = 3  # indoor, outdoor, other

# Model definition
model = models.Sequential()

# 2D CNN layers applied to each frame
model.add(layers.TimeDistributed(layers.Conv2D(32, (3, 3), activation='relu'), 
                                 input_shape=(frame_count, frame_height, frame_width, channels)))
model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))
model.add(layers.TimeDistributed(layers.Conv2D(64, (3, 3), activation='relu')))
model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))
model.add(layers.TimeDistributed(layers.Flatten()))

# Temporal analysis
model.add(layers.Conv1D(128, 3, activation='relu'))
model.add(layers.GlobalMaxPooling1D())

# Classification layer
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()
