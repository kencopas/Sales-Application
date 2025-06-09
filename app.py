import os

from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
from dotenv import load_dotenv

from data_client import DataClient

load_dotenv()
app = Flask(__name__)
dc = DataClient()


def send_sms(body, to):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_= os.getenv('TWILIO_PHONE_NUMBER'),
        to=to
    )

    return message.sid

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
