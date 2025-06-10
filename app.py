from flask import Flask, request, render_template, jsonify, abort
from twilio.rest import Client
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

from utils.logging import gotenv, debug
from data_client import DataClient
from constants import INDEX_VARS
import setup

load_dotenv()
setup.init()
app = Flask(__name__)
_dc = None


@app.route("/view-database")
def private_endpoint():
    """
    View the database information
    """
    # Retrieve the environment variables
    private_token = gotenv('PRIVATE_API_TOKEN')
    database = gotenv('MYSQL_DATABASE')
    table = gotenv('MYSQL_TABLE')

    # Retrieve the token from the url
    token = request.args.get("token")

    # Check if the token matches the private api token env variable
    if token != private_token:
        abort(403)

    # Retrieve the DataClient, select the database, and select all rows
    dc = get_dc()
    dc.sql.run(f'USE {database};')
    output = dc.sql.run(f'SELECT * FROM {table};')

    # If the table is not empty, pass data to view-database.html template
    if output:
        columns = output[0]
        rows = output[1:]
        return render_template(
            "display-leads.html",
            rows=rows,
            columns=columns
        )
    else:
        return f"Empty table {table}"


@debug
def get_dc() -> DataClient:
    global _dc
    if _dc is None:
        _dc = DataClient()
    return _dc


@debug
def send_twilio(body, to):
    account_sid = gotenv('TWILIO_ACCOUNT_SID')
    auth_token = gotenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=gotenv('TWILIO_PHONE_NUMBER'),
        to=to
    )

    return message.sid


@debug
def send_sms(phone_number, message):

    gmail_user = gotenv('SMTP_GMAIL')
    app_pass = gotenv('SMTP_APP_PASS')
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


# Render index.html at the root url
@debug
@app.route("/")
def home():
    # Retrieve all specified environment variables and pass to index.html
    index_kwargs = {key: gotenv(key.upper()) for key in INDEX_VARS}
    return render_template("index.html", **index_kwargs)


@app.route("/quote_submit", methods=['POST'])
def quote_submit():
    """
    Quote Submission Endpoint

    Takes information optionally, passes to DataClient, renders a template
    """

    if request.form:

        info = request.form.to_dict()

        # Print and save the user info
        print(info)
        get_dc().handle_submit(info)

    return render_template("quote-submitted.html")


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
