# api_client.py
#
# Usage from command line:
# curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" -d '{"bathrooms": "2", "bedrooms": "3", "sqft_living": "1800", "sqft_lot": "2200", "floors": "1", "waterfront": "1", "condition": "3"}'
#
import requests


def make_request():
    """Make a request to the API server"""

    url = "http://127.0.0.1:5000"

    data = {
        "bathrooms": "2",
        "bedrooms": "3",
        "sqft_living": "1800",
        "sqft_lot": "2200",
        "floors": "1",
        "waterfront": "1",
        "condition": "3",
    }

    response = requests.post(url, json=data, timeout=5)

    print(response.text)


if __name__ == "__main__":
    make_request()
    
    
    
 #   OE PASEN TRAINMODEL Y WEB_APP
 
 
 #web_app.py
 


import pickle

import pandas as pd  # type: ignore
from flask import Flask, render_template, request  # type: ignore

app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=("GET", "POST"))
def index():
    """Main web page"""

    if request.method == "POST":

        user_values = {}

        # Lee los valores de las cajas de texto de la interfaz
        user_values["bedrooms"] = float(request.form["bedrooms"])
        user_values["bathrooms"] = float(request.form["bathrooms"])
        user_values["sqft_living"] = float(request.form["sqft_living"])
        user_values["sqft_lot"] = float(request.form["sqft_lot"])
        user_values["floors"] = float(request.form["floors"])

        if request.form.get("waterfront") == "Yes":
            user_values["waterfront"] = 0
        else:
            user_values["waterfront"] = 1

        #
        # Valore entre 1 y 5
        if request.form.get("condition") == "1":
            user_values["condition"] = 1
        elif request.form.get("condition") == "2":
            user_values["condition"] = 2
        elif request.form.get("condition") == "3":
            user_values["condition"] = 3
        elif request.form.get("condition") == "4":
            user_values["condition"] = 4
        else:
            user_values["condition"] = 5

        df = pd.DataFrame.from_dict(user_values, orient="index").T

        with open("homework/house_predictor.pkl", "rb") as file:
            loaded_model = pickle.load(file)

        prediction = round(loaded_model.predict(df)[0][0], 2)

    else:
        prediction = None

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)
    
# train_model.py
"""Build, deploy and access a model using scikit-learn"""

import pickle

import pandas as pd  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore

df = pd.read_csv("files\input\house_data.csv", sep=",")

features = df[
    [
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "sqft_lot",
        "floors",
        "waterfront",
        "condition",
    ]
]

target = df[["price"]]

estimator = LinearRegression()
estimator.fit(features, target)

with open("homework/house_predictor.pkl", "wb") as file:
    pickle.dump(estimator, file)