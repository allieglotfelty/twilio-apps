from flask import Flask, request, redirect
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

callers = {
    "+1603*******": "Allie Glotfelty"
}

@app.route("/", methods=["GET", "POST"])
def hello_monkey():
    """Respond to incoming requests."""

    # Get caller's phone number from the incoming Twilio request
    from_number = request.values.get("From", None)
    if from_number in callers:
        caller = callers[from_number]
    else:
        caller = "Monkey"

    resp = VoiceResponse()

    # Greet caller
    resp.say("Hello " + caller)

    # Play MP3 for them:
    resp.play(" http://demo.twilio.com/hellomonkey/monkey.mp3 ")

    # Gather digits.
    g = Gather(numDigits=1, action="/handle-key", method="POST")

    # Say a command and listen for the caller to press a key. When they press a
    # key, redirect them to /handle-key
    g.say("To speak to a real monkey, press 1. Press 2 to record your own monkey howl. Press any other key to start over.")
    resp.append(g)

    return str(resp)


@app.route("/handle-key", methods=["GET", "POST"])
def handle_key():
    """Handle key press from a user."""

    #Get the digit pressed by the user
    digit_pressed = request.values.get("Digits", None)

    if digit_pressed == "1":
        resp = VoiceResponse()

        # Dial (310) 555-1212 - connect that number to the incoming caller.
        resp.dial("+13105551212")
        #If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")

        return str(resp)

    elif digit_pressed == "2":
        resp = VoiceResponse()
        resp.say(" Record your monkey howl after the tone. ")
        resp.record(maxLength="30", action="/handle-recording")
        return str(resp)

        # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")

@app.route("/handle-recording", methods=["GET", "POST"])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get("RecordingUrl", None)
    print recording_url
    resp = VoiceResponse()
    resp.say(" Thanks for howling... take a listen to what you howled. ")
    resp.play(recording_url)
    resp.say(" Goodbye. ")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
