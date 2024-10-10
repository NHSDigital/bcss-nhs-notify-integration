import uuid
import json
from time import time
import jwt  # https://github.com/jpadilla/pyjwt
import requests
import constants
from dotenv import dotenv_values
from flask import Flask, render_template, request, url_for, redirect, jsonify

import os
from services.BCSSCommsManager import BCSSCommsManager

### You will need to set up local env variables

config = dotenv_values(".env")
app = Flask(__name__)

bcss_comms_manager = BCSSCommsManager()

@app.route('/send-pre-invitation', methods=['POST'])
def send_pre_invitation():
    request_data = request.get_json() 

    if not request_data:
        return jsonify({"error": "Invalid input"}), 400

    recipients = request_data.get('data') 

    response = bcss_comms_manager.send_pre_inviation(os.getenv("ROUTING_PLAN_ID"), recipients)

    return jsonify(response["data"]), 200

@app.route('/message-status/<message_id>', methods=['GET'])
def get_message_status(message_id: str):
    
    response = bcss_comms_manager.get_message_status(message_id)

    return jsonify(response), 200


@app.route("/get_nhs_app_details/<ods_code>/<page_number>", methods=["GET"])
def get_nhs_app_details(ods_code: str, page_number: int):
    response = bcss_comms_manager.get_nhs_app_account_details(ods_code, page_number)
    return response


@app.route("/")
def main():
    if request.method == "POST":
        message_id = request.form.get("messageID")
        return redirect(url_for("get_message_status", messageID=message_id))
    return render_template(
        "index.html",
    )


if __name__ == "__main__":
    app.run(debug=True)
    main()

### TO DO:
# Decouple JWT Gen and Authentication from API calls, own files probably (Uzairs refactoring a good start)
# Clean up duplicate code, move Notify headers etc. into own file
# Add between pages at least for POST requests to paste in message bodies rather than hard coded
# Take any request payload content into own folder (examples?)
# Can probably put endpoint strings in variables too
