import requests

# https://ex-api.botorange.com/contact/list?token=6214b16a39011db76498866b&current=1&pageSize=4

# curl -X GET "https://ex-api.botorange.com/contact/list?token=6214b16a39011db76498866b&current=1&pageSize=10"

# curl -X GET "https://ex-api.botorange.com/contact/list?token=6214b16a39011db76498866b&current=0&pageSize=10"

token = "6214b16a39011db76498866b"
url = "https://ex-api.botorange.com/contact/list?token=%s&current=1&pageSize=4" % token
# url = "https://hub.juzibot.com/api/v1/instantReply/getChatId?token=%s" % token
res = requests.get(url)
print(res.text)