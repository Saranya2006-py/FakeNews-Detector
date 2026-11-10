from lime.lime_text import LimeTextExplainer
import pickle

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

explainer = LimeTextExplainer(class_names=["Fake","Real"])

def explain_prediction(text):

    def predict_prob(texts):

        vectors = vectorizer.transform(texts)

        return model.predict_proba(vectors)

    explanation = explainer.explain_instance(
        text,
        predict_prob,
        num_features=6
    )

    return explanation.as_list()