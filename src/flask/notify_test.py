import uuid
import json
from time import time
import jwt  # https://github.com/jpadilla/pyjwt
import requests
import constants
from dotenv import dotenv_values
from flask import Flask, render_template, request, url_for, redirect

### You will need to set up local env variables

config = dotenv_values(".env")
app = Flask(__name__)


def generate_jwt():
    ########## Generate JWT ##########
    with open(config["PRIVATE_KEY_PATH"], "r", encoding="utf-8") as f:
        private_key = f.read()

    claims = {
        "sub": config["API_KEY"],
        "iss": config["API_KEY"],
        "jti": str(uuid.uuid4()),
        "aud": "https://int.api.service.nhs.uk/oauth2/token",
        "exp": int(time()) + 300,  # 5mins in the future
    }

    additional_headers = {"kid": config["KID"]}

    j = jwt.encode(claims, private_key, algorithm="RS512", headers=additional_headers)

    return j


def get_access_token(jwt):
    ########## Get access token ##########
    token_request_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_request_body = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": jwt,
    }

    token_response = requests.post(
        config["TOKEN_URL"], data=token_request_body, headers=token_request_headers
    )
    token_response_text = json.loads(token_response.text)
    access_token = token_response_text["access_token"]

    return access_token


@app.route("/create_message_batch")
def create_message_batch():
    jwt = generate_jwt()
    access_token = get_access_token(jwt)
    ########## Notify API call ##########
    notify_headers = {
        "Content-Type": constants.NHS_CONTENT_TYPE,
        "Accept": constants.NHS_CONTENT_TYPE,
        "Authorization": constants.AUTHORIZATION_TYPE + access_token,
        "X-Correlation-Id": str(uuid.uuid4()),
    }
    message_batch_reference = "0e8a0d1d-5fa3-4bfd-ac9f-9c3229411574"
    message_batch_body = {
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": config["ROUTING_PLAN_ID"],
                "messageBatchReference": message_batch_reference,
                "messages": [
                    {
                        "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "1932-01-06",
                        },
                        "originator": {"odsCode": "X26"},
                        "personalisation": {"custom": "value"},
                    }
                ],
            },
        }
    }

    notify_response = requests.post(
        config["NOTIFY_INT_URL"] + "/v1/message-batches",
        data=json.dumps(message_batch_body),
        headers=notify_headers,
    )
    return render_template(
        "jsonresponse.html",
        responseCode=notify_response.status_code,
        responseJSON=json.dumps(notify_response.json(), indent=4),
    )


@app.route("/create_message_single")
def create_single_message():
    ########## Notify API call ##########
    jwt = generate_jwt()
    access_token = get_access_token(jwt)
    notify_headers = {
        "Content-Type": constants.NHS_CONTENT_TYPE,
        "Accept": constants.NHS_CONTENT_TYPE,
        "Authorization": constants.AUTHORIZATION_TYPE + access_token,
        "X-Correlation-Id": str(uuid.uuid4()),
    }
    message_reference = "e69744f8-d288-4e27-b5fb-25c7c6f8cb14"
    message_batch_body = {
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": config["ROUTING_PLAN_ID"],
                "messageReference": message_reference,
                "recipient": {"nhsNumber": "9990548609", "dateOfBirth": "1932-01-06"},
                "originator": {"odsCode": "X26"},
                "personalisation": {"custom": "value"},
            },
        }
    }

    notify_response = requests.post(
        config["NOTIFY_INT_URL"] + "/v1/messages",
        data=json.dumps(message_batch_body),
        headers=notify_headers,
    )
    return render_template(
        "jsonresponse.html",
        responseCode=notify_response.status_code,
        responseJSON=json.dumps(notify_response.json(), indent=4),
    )


@app.route("/get_message_status", methods=["GET", "POST"])
def get_message_status():
    if request.method == "POST":
        jwt = generate_jwt()
        access_token = get_access_token(jwt)
        notify_headers = {
            "Content-Type": constants.NHS_CONTENT_TYPE,
            "Accept": constants.NHS_CONTENT_TYPE,
            "Authorization": constants.AUTHORIZATION_TYPE + access_token,
            "X-Correlation-Id": str(uuid.uuid4()),
        }

        message_id = request.form.get("messageID")
        notify_response = requests.get(
            config["NOTIFY_INT_URL"] + "/v1/messages/" + message_id,
            headers=notify_headers,
        )
        return render_template(
            "jsonresponse.html",
            responseCode=notify_response.status_code,
            responseJSON=json.dumps(notify_response.json(), indent=4),
        )
    return render_template(
        "jsonresponse.html",
        responseCode="SOMETHING WENT WRONG",
        responseJSON="CHECK THE DEBUGS",
    )


@app.route(
    "/get_nhs_app_details", methods=["GET", "POST"]
)  ####### STARTING POINT FOR TOMORROW
def get_nhs_app_details():
    if request.method == "POST":
        jwt = generate_jwt()
        access_token = get_access_token(jwt)
        notify_headers = {
            "Content-Type": constants.NHS_CONTENT_TYPE,
            "Accept": constants.NHS_CONTENT_TYPE,
            "Authorization": constants.AUTHORIZATION_TYPE + access_token,
            "X-Correlation-Id": str(uuid.uuid4()),
        }

        ods_code = request.form.get("ODSCode")
        page_number = request.form.get("PageNumber")
        params = {"ods-organisation-code": ods_code, "page": page_number}
        notify_response = requests.get(
            config["NOTIFY_INT_URL"] + "/channels/nhsapp/accounts",
            headers=notify_headers,
            params=params,
        )
        return render_template(
            "jsonresponse.html",
            responseCode=notify_response.status_code,
            responseJSON=json.dumps(notify_response.json(), indent=4),
        )
    return render_template("jsonresponse.html")


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
