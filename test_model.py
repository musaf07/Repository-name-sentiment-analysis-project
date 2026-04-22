import pickle

# load model + vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

# test
print("Prediction for 'bad':", model.predict(vectorizer.transform(["bad"])))
print("Prediction for 'good':", model.predict(vectorizer.transform(["good"])))