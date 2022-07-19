# -*- coding: utf-8 -*-
"""NLP_deploy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YfsfFq1Uw1im1zKxWRV9zp41pbSWdkpv
"""

import os
import re
import json
import pickle
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

TOKENIZER_LOAD_PATH = os.path.join(os.getcwd(), 'tokenizer.json')
NLP_LOAD_PATH = os.path.join(os.getcwd(), 'nlp.h5')
OHE_LOAD_PATH = os.path.join(os.getcwd(), 'ohe.pkl')

"""tokenizer"""

with open(TOKENIZER_LOAD_PATH, 'r') as file:
  loaded_tokenizer = json.load(file)

tokenizer = tokenizer_from_json(loaded_tokenizer)

"""ohe"""

with open(OHE_LOAD_PATH, 'rb') as file:
  ohe = pickle.load(file)

"""nlp"""

nlp = load_model(NLP_LOAD_PATH)
nlp.summary()

"""DATA LOADING"""

new_review = "Another Biggie from the Deadpool franchise hits hard! Goosebumping effects and stunts make it worth taking the day-off for. Amazing performance from the whole cast, everyone was just perfect in his/her space. Sense of humour was always perfect and r rated movies from marvel-20th century is unusual but it's like they have perfected that too. Every piece of the story was perfectly timelined and placed/explained. The conversations amongst wade and his wife could have been a little dramatic because it breaks the funny flow/vibe of the movie all along but the idea of saving the child for his own better future is beautiful. Even this is kind of satisfying and fairy-likewhn wade hits lows and meets his wif e for help like a pixie to a princess. Anyways, the movie does have some fairytale stuff unlike the first part but still is great."

new_review = [input('Please write your feedback here:')]

"""DATA CLEANING"""

for index, text in enumerate(new_review):
  # to remove html tags
  # anything within the <> will be removed including <>
  # ? to tell re dont be greedy so it wont capture anything
  # from the first < to the last > in the document
  new_review = re.sub('<.*?>','',text)
  new_review = re.sub('[^a-zA-Z]',' ',new_review).lower().split()

"""DATA PREPROCESSING"""

new_review = tokenizer.texts_to_sequences(new_review)
new_review = np.reshape(new_review,(1, len(new_review)))
new_review = pad_sequences(new_review, 
                           maxlen=178,
                           padding = 'post',
                           truncating = 'post')

"""MODEL PREDICTION"""

outcome = nlp.predict(new_review)
print('This review is {}'.format(ohe.inverse_transform(outcome)[0][0]))

