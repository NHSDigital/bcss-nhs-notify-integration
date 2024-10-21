from time import time
from dotenv import dotenv_values
from flask import Flask, render_template, request, url_for, redirect, jsonify

import os
from services.BCSSCommsManager import BCSSCommsManager

config = dotenv_values(".env")
app = Flask(__name__)

bcss_comms_manager = BCSSCommsManager()


@app.route("/send-pre-invitation", methods=["POST"])
def send_pre_invitation():
    request_data = request.get_json()

    if not request_data:
        return jsonify({"error": "Invalid input"}), 400

    recipients = request_data.get("data")

    response = bcss_comms_manager.send_pre_invitation(
        os.getenv("ROUTING_PLAN_ID"), recipients
    )

    return jsonify(response["data"]), 200


@app.route("/message-status/<message_id>", methods=["GET"])
def get_message_status(message_id: str):
    response = bcss_comms_manager.get_message_status(message_id)

    return jsonify(response), 200


@app.route("/get_nhs_app_details/<ods_code>/<page_number>", methods=["GET"])
def get_nhs_app_details(ods_code: str, page_number: int):
    response = bcss_comms_manager.get_nhs_app_account_details(ods_code, page_number)
    return response


@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    main()
