import json

import requests

from config import *

path = '/pan/api/spaces?orgId={}&memberId={}'


def get_space_id(orgid, memberid):
    res = requests.get(host + path.format(orgid, memberid), cookies=cookies)
    obj = json.loads(res.text)
    # 这里比较暴力, todo
    data = obj[0]
    return data['spaceId'], data['rootId'], data['name']
