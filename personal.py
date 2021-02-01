import base64
import json

import requests

from config import *

url = 'https://www.teambition.com/api/organizations/personal'


def get_org_id():
    res = requests.get(url, cookies=cookies)
    return json.loads(res.text)['_id']


def get_uid():
    teambition_sessionid = cookies.get('TEAMBITION_SESSIONID')
    base64_str = base64.b64decode(teambition_sessionid).decode()
    obj = json.loads(base64_str)
    return obj['uid']
