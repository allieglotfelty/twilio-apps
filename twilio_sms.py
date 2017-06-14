from flask import Flask, request, redirect, session
from twilio.twiml.messaging_response import MessagingResponse, Message

SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

callers = {
    "+16032750521": "Allie"
}

@app.route("/", methods=["GET", "POST"])
def hello_monkey():
    """Respond with the number of text messages sent between two parties."""

    counter = session.get('counter', 0)

    # Increment the counter
    counter += 1

    # Save the new counter to the session
    session['counter'] = counter

    from_number = request.values.get("From")
    if from_number in callers:
        name = callers[from_number]
    else:
        name = "Monkey"

    msg = "".join([name, " has messaged ", request.values.get("To"), " ", str(counter), " times."])

    resp = MessagingResponse()
    resp.message(body=msg)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
