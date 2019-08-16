from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import numpy as np
import os
os.environ['TF_[CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from nltk import word_tokenize
from konlpy.tag import Okt
import tensorflow as tf

okt = Okt()

char2Idx = {}
case2Idx = {'numeric': 0, 'allLower': 1, 'allUpper': 2, 'initialUpper': 3, 'other': 4, 'mainly_numeric': 5,
            'contains_digit': 6, 'PADDING_TOKEN': 7}

# ::Hard coded char lookup ::
char2Idx = {"PADDING": 0, "UNKNOWN": 1}
for c in " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,-_()[]{}!?:;#'\"/\\%$`&=*+@^~|":
    char2Idx[c] = len(char2Idx)

f = open("data2/char_index.txt", "r", encoding='UTF-8')
char_index = f.read()

for c in char_index:
    char2Idx[c] = len(char2Idx)
# :: Hard coded case lookup ::


loc = os.path.dirname(os.path.realpath(__file__))

print('loc', loc)
# model = load_model(os.path.join(loc,"models/model.h5"))
# loading word2Idx
word2Idx = np.load(os.path.join(loc, "models/word2Idx.npy"), allow_pickle=True).item()
# loading idx2Label
idx2Label = np.load(os.path.join(loc, "models/idx2Label.npy"), allow_pickle=True).item()

model = load_model(os.path.join(loc, "models/model.h5"))
model._make_predict_function()
graph = tf.get_default_graph()


def getCasing(word, caseLookup):
    casing = 'other'

    numDigits = 0
    for char in word:
        if char.isdigit():
            numDigits += 1

    digitFraction = numDigits / float(len(word))

    if word.isdigit():  # Is a digit
        casing = 'numeric'
    elif digitFraction > 0.5:
        casing = 'mainly_numeric'
    elif word.islower():  # All lower case
        casing = 'allLower'
    elif word.isupper():  # All upper case
        casing = 'allUpper'
    elif word[0].isupper():  # is a title, initial char upper, then all lower
        casing = 'initialUpper'
    elif numDigits > 0:
        casing = 'contains_digit'
    return caseLookup[casing]


def createTensor(sentence, word2Idx, case2Idx, char2Idx):
    unknownIdx = word2Idx['UNKNOWN_TOKEN']

    wordIndices = []
    caseIndices = []
    charIndices = []

    for word, char in sentence:
        word = str(word)
        if word in word2Idx:
            wordIdx = word2Idx[word]
        elif word.lower() in word2Idx:
            wordIdx = word2Idx[word.lower()]
        else:
            wordIdx = unknownIdx
        charIdx = []
        for x in char:
            if x in char2Idx.keys():
                charIdx.append(char2Idx[x])
            else:
                charIdx.append(char2Idx['UNKNOWN'])
        wordIndices.append(wordIdx)
        caseIndices.append(getCasing(word, case2Idx))
        charIndices.append(charIdx)

    return [wordIndices, caseIndices, charIndices]


def addCharInformation(sentence):
    return [[word, list(str(word))] for word in sentence]


def padding( Sentence):
    Sentence[2] = pad_sequences(Sentence[2], 52, padding='post')
    return Sentence


def predict(Sentence):

    Sentence = words = okt.morphs(Sentence)  # 단어 토큰화
    print('Sentence', Sentence)
    Sentence = addCharInformation(Sentence)
    Sentence = padding(createTensor(Sentence, word2Idx, case2Idx, char2Idx))
    tokens, casing, char = Sentence
    tokens = np.asarray([tokens])
    casing = np.asarray([casing])
    char = np.asarray([char])
    print('tokens', tokens)
    print('casing', casing)
    print('char', char)

    pred = model.predict([tokens, casing, char], verbose=False)[0]

    pred = pred.argmax(axis=-1)

    print('dict', idx2Label)

    pred = [idx2Label[x].strip() for x in pred]

    return list(zip(words, pred))


def index(request):
    return render(request, 'index.html')


def vote2(request):
    #print(predict('안녕 안녕 하이 방가'))
    #print(request.POST['nerText'])
    txt = request.POST['nerText']
    returnText = predict(txt)



    return render(request, 'index.html', {'result': returnText})

    #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


