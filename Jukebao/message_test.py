import pandas as pd
import requests
import json

url = "https://ex-api.botorange.com/message/send"

# curl -X GET "https://ex-api.botorange.com/contact/list?token=6214b16a39011db76498866b&current=1&pageSize=4"

# 通过联系人列表可以获取 chatid  
# GET https://ex-api.botorange.com/contact/list?token={your-token}&current=1&pageSize=4 


data = {
  "chatId": "6214b19ea66c67d78d0f15ef",
  "token": "6214b16a39011db76498866b",
  "messageType": 0 , # MessageType, check below
  "payload": {
    "text": "测试信息请忽略",
    "mention": [] # mention list, you can only set it when you send text message to room,
  },
  "externalRequestId": "1", # nullable, 会在回调中原样带回的字段，需要保证唯一（当不唯一时报错）
}
# data = json.dumps(data)
# data = {
#     'a': 123,
#     'b': 456
# }

## headers中添加上content-type这个参数，指定为json格式
headers = {'Content-Type': 'application/json'}

## post的时候，将data字典形式的参数用json包转换成json格式。
res = requests.post(url=url, headers=headers, data=json.dumps(data))

print(res.text)