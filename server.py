from flask import Flask
from flask import jsonify, request
import pandas as pd
import uuid
import os

app = Flask(__name__)

@app.route("/")
def hello():
	dic = {"response": "Hello World!"}
	return jsonify(dic)

# GET METHODS

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
	df = pd.read_csv("dataset.csv")
	df.drop('Unnamed: 0', inplace=True, axis=1)
	js = df.to_json(orient="records")
	return js

@app.route("/leaderboard/<country_iso_code>", methods=["GET"])
def leaderboardByCountry(country_iso_code):
	df = pd.read_csv("dataset.csv")
	df.drop('Unnamed: 0', inplace=True, axis=1)
	df = df[df['country'] == country_iso_code]
	js = df.to_json(orient="records")
	return js

@app.route("/user/profile/<user_guid>", methods=["GET"])
def userProfile(user_guid):
	df = pd.read_csv("dataset.csv")
	df.drop('Unnamed: 0', inplace=True, axis=1)
	df = df[df['user_id'] == user_guid]
	js = df.to_json(orient="records")
	return js

# POST METHODS

@app.route("/score/submit", methods=["POST"])
def scoreSubmit():
    df = pd.read_csv("dataset.csv")
    df.drop('Unnamed: 0', inplace=True, axis=1)
    user = request.form['user_id']
    score = request.form["score_worth"]
    timestamp = request.form["timestamp"]
    userRow = df[df['user_id'] == str(user)]
    print(userRow.head())
    new_row = {"response": "This is not the highest"}
    if int(userRow["scores"]) < int(score):
        new_row = {'scores': int(score), 'country':userRow["country"], 'user_id':str(user), 'display_name':userRow["display_name"]}
        add_df = pd.DataFrame(new_row, columns=["scores", "country", "user_id", "display_name"])
        df = df[df['user_id'] != str(user)]
        df = df.append(add_df, ignore_index=True)
        df['rank'] = df['scores'].rank(method="min", ascending=False)
        df.to_csv('dataset.csv')
        return jsonify({"response": "ok"})
    return jsonify({"response": "This is not the highest"})

@app.route("/user/create", methods=["POST"])
def userSubmit():
    df = pd.read_csv("dataset.csv")
    df.drop('Unnamed: 0', inplace=True, axis=1)
    user = uuid.uuid1()
    score = 0
    display_name = request.form["display_name"]
    country = request.form["country"]
    new_row = {'scores': [int(score)], 'country':[str(country)], 'user_id':[str(user)], 'display_name':[str(display_name)]}
    add_df = pd.DataFrame(new_row, columns=["scores", "country", "user_id", "display_name"])
    df = df.append(add_df, ignore_index=True)
    df['rank'] = df['scores'].rank(method="min", ascending=False)
    df.to_csv('dataset.csv')
    return jsonify({"response": "ok"})

if __name__ == "__main__":
    if not os.path.isfile("dataset.csv"):
        dicc = {"scores":[], "country":[], "user_id":[], "display_name":[]}
        df_first = pd.DataFrame(dicc, columns=["scores", "country", "user_id", "display_name"])
        df_first.to_csv("dataset.csv")
    app.run(host="0.0.0.0", port=80)
