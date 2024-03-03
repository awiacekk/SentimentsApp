import numpy as np
import string
from keras.layers import TextVectorization

from spellchecker import SpellChecker

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from keras.models import load_model
import pickle
from sklearn.feature_selection import SelectPercentile, chi2


class Models:
    def __init__(self):
        self.vectorizer = None
        self.sp = None
        self.model1 = None
        self.model2 = None
        self.dict = {0: 'negative', 1: 'positive'}
        self.sc = SpellChecker()
        self.stemmer = SnowballStemmer(language='english')

    def loadSavedModels(self, file):
        self.model1 = load_model(file+"/sentiment_model.h5")
        self.model2 = load_model(file+"/sentiment_model_with_fetures.h5")
        x_train = np.load(file+"/x_train.npy")
        y_train = np.load(file+"/y_train.npy")
        self.sp = SelectPercentile(chi2, percentile=10).fit(x_train, y_train)
        from_disk = pickle.load(open(file+"/vectorizer.pkl", "rb"))
        self.vectorizer = TextVectorization.from_config(from_disk['config'])
        self.vectorizer.set_weights(from_disk['weights'])

    def remove_punc(self, sentance):
        return sentance.translate(str.maketrans('', '', string.punctuation))

    def correct(self, sentance):
        misspelled = self.sc.unknown(str(sentance).split())
        correct = [self.sc.correction(w) if w in misspelled else w for w in sentance.split()]
        return " ".join(filter(lambda c: c is not None, correct))

    def remove_stop(self, sentance):
        correct = [w for w in sentance.split() if w not in stopwords.words('english')]
        return " ".join(correct)

    def stemming(self, sentance):
        correct = [self.stemmer.stem(w) for w in sentance.split()]
        return " ".join(correct)

    def remove_numbers(self, sentance):
        return " ".join([s for s in sentance.split() if not s.isdigit()])

    def prepare_data(self, sentance, vectorizer=None):
        sentance = sentance.lower()
        sentance = self.remove_punc(sentance)
        sentance = self.correct(sentance)
        sentance = self.remove_stop(sentance)
        sentance = self.stemming(sentance)
        if vectorizer is None:
            return sentance
        else:
            return np.asarray(vectorizer(sentance).numpy(), dtype='float32').reshape(1, -1)

    def predict_sentiment(self, sentance, model, feature_selection=None):
        if feature_selection is None:
            data = self.prepare_data(sentance, self.vectorizer)
        else:
            data = feature_selection.transform(self.prepare_data(sentance, self.vectorizer))
        prediction = np.round(model.predict(data))
        return self.dict.get(prediction.item())

    def calculateModel1(self, text):
        sentiment = self.predict_sentiment(text, self.model1)
        return sentiment

    def calculateModel2(self, text):
        data = self.prepare_data(text, self.vectorizer)
        new_data = self.sp.transform(data)
        print(new_data.shape)
        prediction = np.round(self.model2.predict(new_data))
        return self.dict.get(prediction.item())
