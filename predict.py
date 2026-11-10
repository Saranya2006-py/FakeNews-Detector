import pickle
from preprocessing import clean_text

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

def predict_news(text):

    text = clean_text(text)

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)

    probability = model.predict_proba(vector)[0]

    if prediction == 1:
        label = "Real News"
    else:
        label = "Fake News"

    return label, probability