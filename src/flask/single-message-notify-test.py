import uuid
import jwt  # https://github.com/jpadilla/pyjwt
import requests
import json
from time import time
from flask import Flask, render_template
from dotenv import dotenv_values

#stolen from tom :D
def create_message(access_token):
    ########## Notify API call ########## 
    notify_headers = {
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json",
      "Authorization": "Bearer " + access_token,
      "X-Correlation-Id": str(uuid.uuid4()),
    }
    message_reference = "e69744f8-d288-4e27-b5fb-25c7c6f8cb14"
    message_batch_body = {
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": config['ROUTING_PLAN_ID'],
                "messageReference": message_reference,
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "1932-01-06"
                },
                "originator": {
                    "odsCode": "X26"
                },
                "personalisation": {
                    "custom" : "value"
                }
            }
            }
        }

    notify_response = requests.post(config['NOTIFY_INT_URL']+"/v1/messages", data = json.dumps(message_batch_body), headers = notify_headers)
    return notify_response
