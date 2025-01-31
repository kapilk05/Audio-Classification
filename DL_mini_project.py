# -*- coding: utf-8 -*-
"""Audio_Classification.ipynb

Automatically generated by Colab.

Original file is located at 
    https://colab.research.google.com/github/maitreya-v/Audio-Classification-Librosa/blob/main/Audio_Classification.ipynb
""" 

import tensorflow as tf

# Check if a GPU is available
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("No GPU found")

# Set TensorFlow to use GPU memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Enable GPU memory growth
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU memory growth enabled")
    except RuntimeError as e:
        print(e)

import tensorflow as tf

# Check if a GPU is available and print its name
if tf.test.is_gpu_available():
    print("Default GPU Device: {}".format(tf.test.gpu_device_name()))
else:
    print("No GPU available")

from google.colab import drive
drive.mount('/content/drive')

# /content/drive/MyDrive/audio

import numpy as np
import pandas as pd
import librosa
import librosa.display
import IPython.display as ipd
import matplotlib.pyplot as plt
from tqdm import tqdm

audio_df=pd.read_csv('./UrbanSound8K.csv')

audio_df.head(25)

filename='/content/drive/MyDrive/audio/fold1/101415-3-0-2.wav'

data,sr=librosa.load(filename)

data

sr

ipd.Audio(filename)

plt.figure(figsize=(14,5))
data,sr=librosa.load(filename)
librosa.display.waveshow(data,sr=sr)
plt.title('Dog barking')
plt.show()

data_trimmed,unknown=librosa.effects.trim(data,top_db=20)
plt.figure(figsize=(14,5))
plt.title('Trimmed Dog Barking Audio')
librosa.display.waveshow(data_trimmed)

audio_df['class'].value_counts()

audio_df.head()

mfcc_feature=librosa.feature.mfcc(y=data,sr=sr,n_mfcc=20)

scaled_feature = np.mean(mfcc_feature.T,axis=0)
scaled_feature

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
sc.fit_transform(mfcc_feature)

audio_df.iloc[0]['slice_file_name']

def get_path(index):
  standard_path='/content/drive/MyDrive/audio/fold'
  folder_id=audio_df.iloc[index]['fold']
  filename=audio_df.iloc[index]['slice_file_name']
  full_path=str(standard_path) + str(folder_id) + '/' + str(filename)
  return full_path

# L=[]
# for index,row in tqdm(audio_df.iterrows()):
#     path=get_path(index)
#     data,sr=librosa.load(path)
#     mfcc_feature=librosa.feature.mfcc(y=data,sr=sr,n_mfcc=40)
#     mfcc_scaled_feature=sc.fit_transform(mfcc_feature)
#     df_dict={'feature':mfcc_scaled_feature,'class':row['class']}
#     L.append(df_dict)

# final_df=pd.DataFrame(L)
# L

# from google.colab import files
# final_df.to_csv('scaled_audio_feature.csv', index=False)
# files.download('scaled_audio_feature.csv')

try:
  final_df=pd.read_csv('./scaled_audio_features_jupyter.csv')
except ParseError:
  print('parse')

final_df.head()

def get_array(s):
    s = s.strip('[]')
    s = s.split()

    s = [float(i) for i in s]

    arr = np.array(s)
    return arr
final_df['features']=final_df['features'].apply(get_array)
type(np.array(final_df['features'][0]))
X=final_df['features']
X.shape

X=np.array(final_df['features'].tolist())
y=np.array(final_df['class'].tolist())
# np.array(final_df['features'].tolist())

X[2].shape,X.shape,y[0],y.shape

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
le=LabelEncoder()
y=to_categorical(le.fit_transform(y))

y.shape

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.33,random_state=42)

X_train.shape,X_test.shape,y_train.shape,y_test.shape

label_size=y.shape[1]
label_size

model=tf.keras.models.Sequential()
model.add(tf.keras.Input(shape=(40,)))
model.add(tf.keras.layers.Dense(100,activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(200,activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(100,activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(10,activation='softmax'))

model.summary()

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

from tensorflow.keras.callbacks import ModelCheckpoint
from datetime import datetime

num_epochs=100
batch_size=32
checkpointer = ModelCheckpoint(filepath='saved_models/audio_classification.hdf5',
                               verbose=1, save_best_only=True)
model.fit(X_train,y_train,batch_size=batch_size,epochs=num_epochs,validation_data=(X_test,y_test),callbacks=[checkpointer], verbose=1)
start = datetime.now()
duration = datetime.now() - start
print("Training completed in time: ", duration)

test_accuracy=model.evaluate(X_test,y_test,verbose=0)
test_accuracy[1]

predictions=model.predict(X_test)
predictions.shape
predictions[0]

#testing sample audio
data

filename='/content/drive/MyDrive/audio/fold7/99812-1-2-0.wav'
data,sr=librosa.load(filename)
data_features=librosa.feature.mfcc(y=data,sr=sr,n_mfcc=40)
scaled_features=np.mean(data_features.T,axis=0)
scaled_features=scaled_features.reshape(1,-1)
prediction=np.argmax(model.predict(scaled_features))
prediction = np.array(prediction, ndmin=1)
prediction_label=le.inverse_transform(prediction)
print(prediction_label[0])
ipd.Audio(filename)

filename='/content/drive/MyDrive/audio/fold5/100852-0-0-0.wav'
data,sr=librosa.load(filename)
data_features=librosa.feature.mfcc(y=data,sr=sr,n_mfcc=40)
scaled_features=np.mean(data_features.T,axis=0)
scaled_features=scaled_features.reshape(1,-1)
prediction=np.argmax(model.predict(scaled_features))
prediction = np.array(prediction, ndmin=1)
prediction_label=le.inverse_transform(prediction)
print(prediction_label[0])
ipd.Audio(filename)

filename='/content/drive/MyDrive/audio/fold10/100795-3-0-0.wav'
data,sr=librosa.load(filename)
data_features=librosa.feature.mfcc(y=data,sr=sr,n_mfcc=40)
scaled_features=np.mean(data_features.T,axis=0)
scaled_features=scaled_features.reshape(1,-1)
prediction=np.argmax(model.predict(scaled_features))
prediction = np.array(prediction, ndmin=1)
prediction_label=le.inverse_transform(prediction)
print(prediction_label[0])
ipd.Audio(filename)
