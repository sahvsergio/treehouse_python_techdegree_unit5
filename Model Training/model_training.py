from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.models import Sequential
from nltk.stem import WordNetLemmatizer
import nltk
import numpy as np
import json
import pickle
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"


# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

# Load Intents
intents = json.load(open("intents.json"))

# Initialize Data Containers
words = []
classes = []
documents = []
ignore_symbols = ['?', '!', '.', ',']

# Process Each Intent
for intent in intents['intents']:
    for pattern in intent['pattern']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and Remove Duplicates
words = [lemmatizer.lemmatize(word.lower())
         for word in words if word not in ignore_symbols]
words = sorted(set(words))
classes = sorted(set(classes))

# Save Words and Classes
if not os.path.exists('model'):
    os.makedirs('model')

pickle.dump(words, open('model/words.pkl', 'wb'))
pickle.dump(classes, open('model/classes.pkl', 'wb'))

# Create Training Data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(
        word.lower()) for word in word_patterns if word not in ignore_symbols]

    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Shuffle and Convert Training Data
random.shuffle(training)
training = np.array(training, dtype=object)

train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# Build Model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile Model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy",
              optimizer=sgd, metrics=['accuracy'])

# Train Model
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save Model
model.save('model/chatbot_model.keras')
