import os

from flask import Flask, request, render_template, jsonify, abort
from twilio.rest import Client
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

from utils.logging import path_log, debug
from data_client import DataClient

load_dotenv()
app = Flask(__name__)
_dc = None


@app.route("/lead-list")
def private_endpoint():
    token = request.args.get("token")
    if token != os.getenv('PRIVATE_API_TOKEN'):
        abort(403)
    dc = get_dc()
    dc.sql.run('USE usha_database;')
    output = dc.sql.run('SELECT * FROM user_info;')
    if output:
        columns = output[0]
        rows = output[1:]
        return render_template("display-leads.html", rows=rows, columns=columns)
    else:
        return "brent gei"

@app.route("/book", methods=['POST', 'GET', 'OPTIONS'])
def book():
    print('book()')
    return render_template("book.html")


@debug
def get_dc() -> DataClient:
    global _dc
    if _dc is None:
        _dc = DataClient()
    return _dc


@debug
def send_twilio(body, to):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=to
    )

    return message.sid


@debug
def send_sms(phone_number, message):

    gmail_user = os.getenv('SMTP_GMAIL')
    app_pass = os.getenv('SMTP_APP_PASS')
    to_number = f"{phone_number}@tmomail.net"

    if not gmail_user or not app_pass:
        print('environment variables unset')
        print(gmail_user, app_pass)
        return

    msg = MIMEText(str(message))
    msg['From'] = gmail_user
    msg['To'] = to_number
    msg['Subject'] = ' '

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, app_pass)
        server.sendmail(gmail_user, to_number, msg.as_string())
        server.quit()
        print("SMS sent successfully!")
    except Exception as e:
        print("Failed to send SMS:", e)


@app.route("/")
@debug
def home():
    # send_sms('7402722433', 'Hello, welcome to my website!')
    return render_template("index.html")


@app.route("/quote_submit", methods=['POST'])
def quote_submit():
    return render_template("quote-submitted.html")


@debug
@app.route('/user_submit', methods=['POST'])
def handle_info():

    info = request.get_json()

    # Print the user info
    print(request.headers)
    print(info)

    get_dc().save_user_info(info)

    return jsonify({'status': 'recieved'})


@debug
@app.route('/track', methods=['POST'])
def track():

    # Print request DEBUG
    # print("Headers:", request.headers)
    # print("Data:", request.data)  # raw bytes
    # print("Is JSON?", request.is_json)

    # Get user id and event
    event = request.get_json(silent=True)

    # If request.get_json returned None, return an error
    if event is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400

    print(f"Event: {event}")
    return jsonify({'status': 'received'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
