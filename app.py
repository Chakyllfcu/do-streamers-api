from flask import Flask, render_template
from requests import get
from flask import json

app = Flask(__name__)

channels = ['omalitogell','isarockets','chuchoman21','imlogansolo']




@app.route("/")
def index():
    return "Hello World!"


@app.route("/api/<name>")
def show_streamer(name=None):
    streamer = get(f"https://twitchtracker.com/api/channels/summary/{name}").json()
    return streamer


@app.route("/api/streamers")
def show_streamers():   
    counter = 0
    # detail = {}
    result = []
    for channel in channels:
        url = f'https://twitchtracker.com/api/channels/summary/{channel}'
        response = get(url)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            print(type(response_json))
            response_json.update({'name': channel})
            result.append(response_json)
    result.sort(key=lambda c: c["avg_viewers"], reverse=True)

        
    # Serializing json  
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(debug=True, port=3000)