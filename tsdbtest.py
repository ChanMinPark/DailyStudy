# -*- coding: utf-8 -*-
# test.py

import time
import requests
import json

url = "http://127.0.0.1:4242/api/put"

data = {
    "metric": "foo.bar",
    "timestamp": time.time(),
    "value": 2015,
    "tags": {
       "host": "mypc
    }
}

ret = requests.post(url, data=json.dumps(data))

print ret.text
