from flask import Flask, request, render_template, jsonify

from data_client import DataClient
from constants import LEADS_GUI_API

app = Flask(__name__)
dc = DataClient()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/user_submit', methods=['POST'])
def handle_info():

    info = request.get_json()

    # Print the user info
    print(request.headers)
    print(info)

    dc.save_user_info(info)

    return jsonify({'status': 'recieved'})

@app.route('/track', methods=['POST'])
def track(): 
    
    # Print request DEBUG
    print("Headers:", request.headers)
    print("Data:", request.data)  # raw bytes
    print("Is JSON?", request.is_json)

    # Get user id and event
    event = request.get_json(silent=True)

    # If request.get_json returned None, return an error
    if event is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400

    print(f"Event: {event}")
    return jsonify({'status': 'received'})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
