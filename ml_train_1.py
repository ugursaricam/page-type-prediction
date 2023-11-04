import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


def model_comparison(dataset):
    df = pd.read_csv(dataset)

    df = df.dropna(ignore_index=True)

    le = LabelEncoder()
    df["Output"] = le.fit_transform(df["Output"])

    df["description"] = df["title"] + df["content"]

    X = df['description']
    y = df["Output"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    classifiers = {
        "SVM": SVC(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "XGBoost": XGBClassifier(),
        "LightGBM": LGBMClassifier(),
        "MultinomialNB": MultinomialNB()
    }

    for name, classifier in classifiers.items():
        pipe = Pipeline([
            ('vectorizer_tfidf', TfidfVectorizer()),
            ('Classifier', classifier)
        ])

        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)

        print("=" * 50)
        print(f"Classification Report for {name}:")
        scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
        for metric in scoring_metrics:
            scores = cross_val_score(pipe, X, y, cv=10, scoring=metric)
            mean_score = scores.mean()
            print(f"Mean {metric.capitalize()}: {mean_score:.2f}")

model_comparison("web_sites.csv")