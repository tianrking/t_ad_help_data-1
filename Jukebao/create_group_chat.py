import json
import requests

url = "https://ex-api.botorange.com/room/create"
token = "6214b16a39011db76498866b"

data = {
  "token": token,
  "botUserId": "testUserId",
  "userIds": [
    "TJW"
  ],
  "unionIds": [
    "ozynqsulJFCZ2z1aYeS8h-nuasdAAA"
  ],
  "name": "create",
  "greeting": "大家好，这个是新的群",
  "wxids": [
    "wmrRhyBgAA6PKOL7IA2Nbikedjxxxxxx",
    "wmrRhyBgAANQ1O34HRXfVQh17exxxxxx"
  ]
}

headers = {'Content-Type': 'application/json'}

res = requests.post(url=url, headers=headers, data=json.dumps(data))

print(res.text)


# 错误码	说明
# -2	botUserId的bot不存在
# -3	botUserId存在多个机器人
# -4	不是企业微信
# -5	bot不在线
# -6	群聊加载失败
# -7	拉入群聊失败
# -8	和bot不是好友关系
# -9	群聊中已经存在此好友
# -10	群人数达到上限(500)
# -11	bot不在群内
# -12	该群是内部群，不执行此操作
