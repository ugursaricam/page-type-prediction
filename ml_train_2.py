import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_curve, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import joblib

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def base_model(dataset):
    df = pd.read_csv(dataset)

    df = df.dropna()

    le = LabelEncoder()
    df["Output"] = le.fit_transform(df["Output"])

    df["description"] = df["title"] + df["content"]

    X = df['description']
    y = df["Output"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=22)

    pipe = Pipeline([
        ('vectorizer_tfidf', TfidfVectorizer()),
        ('Multi_nb', MultinomialNB())
    ])

    pipe.fit(X, y)

    y_pred = pipe.predict(X_test)

    print(classification_report(y_test, y_pred))

    return pipe

pipe = base_model("web_sites.csv")

joblib.dump(pipe, "testinium.joblib")





