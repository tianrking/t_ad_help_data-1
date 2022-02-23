import requests


token = "6214b16a39011db76498866b"
url = "https://ex-api.botorange.com/contact/list?token=%s&current=1&pageSize=4" % token

res = requests.get(url)
print(res.text)