# coding=UTF-8
import requests
import json
import time

URL_ALERT = "https://oapi.dingtalk.com/robot/send?access_token=890805b979b5fc58571628e5e25c9d0ded2ffcbe23c614e3173a864e248fab1b"


# send the reports by email
def send(msg):

    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }

    message = "imdb report spider:" + "\n" + msg
    stringBody = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [""],
            "isAtAll": "false"
        }
    }
    MessageBody = json.dumps(stringBody)
    result = requests.post(url=URL_ALERT, data=MessageBody, headers=HEADERS)
    print(result.text)

