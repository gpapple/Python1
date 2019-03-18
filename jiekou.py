import requests

url = "http://fanyi.baidu.com/v2transapi"
params = {
    "from":"en",
    "to":"zh",
    "query": "student"
}

r = requests.request("post", url, params=params)

import json
d = json.loads(r.text)
print(d)


