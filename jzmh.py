import requests # only for JZMH

token = "6214b16a39011db76498866b"


def send_message(chatid, text, url = "https://ex-api.botorange.com/message/send"):
    """
    send message to jzmh
    """
    jzmh_data = {
        "chatId":  chatid, #"6214b19ea66c67d78d0f133d",
        "token": token,
        "messageType": 0, # MessageType, check below
        "payload": {
            "text": text, # str(return_data).replace('{',"").replace('}',"") ,
            "mention": [] # mention list, you can only set it when you send text message to room,
        },
        "externalRequestId": "",
    }

    res = requests.post(url=url, json=jzmh_data, timeout=30)
    return res.ok
