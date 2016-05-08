from flask import Flask, request, redirect, session
import twilio.twiml
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def respond():
    return "HI!!!"
    
    
if __name__ == "__main__":
    app.run(debug=True, 
            host=os.getenv('IP', '0.0.0.0'),
            port = int(os.getenv('PORT', '8080')))