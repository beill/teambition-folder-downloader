import json

import requests

from config import *

path = '/pan/api/orgs/{0}?orgId={0}'


def get_drive_id(orgid):
    res = requests.get(host + path.format(orgid), cookies=cookies)
    obj = json.loads(res.text)
    return obj['data']['driveId']
