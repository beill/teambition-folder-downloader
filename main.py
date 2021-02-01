# coding=utf8
import json
import os
import sys

import requests

import devices
import personal
import spaces
from config import *


def get_nodes(nodeid):
    res = requests.get(host + path, params={
        'orgId': orgid,
        'offset': 0,
        'limit': 100000,
        'orderBy': 'name',
        'orderDirection': 'asc',
        'driveId': driveid,
        'spaceId': spaceid,
        'parentId': nodeid,
    }, cookies=cookies)
    data = json.loads(res.text)['data']
    return data


def get_node_detail(nodeid):
    url = '/pan/api/nodes/{}?orgId={}&driveId={}&spaceId={}'
    res = requests.get(host + url.format(nodeid, orgid, driveid, spaceid), cookies=cookies)
    obj = json.loads(res.text)
    return obj


def input_folder(data):
    if len(data) == 0:
        input('-> 此目录为空, <Enter> 退出: ')
        sys.exit()
    ll = [None]
    for o in data:
        s = len(ll)
        print(s, o['name'])
        ll.append(o)
    while True:
        try:
            i = input('-> 请输入序号选择(输入0, 选定当前文件夹): ')
            rt = ll[int(i)]
            break
        except Exception:
            print('-> 同志, 越界了~')
    return rt


def select_folder(nodeid):
    global node_id, base_path

    obj = input_folder(get_nodes(nodeid))
    if obj is None:
        node_id = nodeid
        return
    if obj['kind'] != 'folder':
        node_id = obj['nodeId']
        return
    base_path = base_path + '/' + obj['name']
    select_folder(obj['nodeId'])


def download(url, filename):
    print('-> 开始下载文件', filename, url)
    if os.path.exists(filename):
        if not os.path.exists(filename + '.aria2'):
            print('-> 文件已存在: ' + filename)
            return
    # 下载
    # 可以替换成 idm, aria2
    sys.stdout.flush()
    os.system('aria2c.exe -c -o "' + filename + '" "' + url + '"')

    # popen = subprocess.Popen('aria2c.exe -o "' + filename + '" "' + url + '"',
    #                          stdout=subprocess.PIPE,
    #                          stderr=subprocess.PIPE
    #                          )
    # for out in popen.communicate():
    #     print(out.decode())

    # res = requests.get(url, stream=True)
    # # 'Transfer-Encoding': 'chunked'
    # clen = int(res.headers.get('Content-Length'))
    # progress_bar = tqdm(total=clen, unit='iB', unit_scale=True)
    # with open(filename, 'wb') as f:
    #     for chunk in res.iter_content(1024 * 1024 * 4):
    #         f.write(chunk)
    #         progress_bar.update(len(chunk))
    # progress_bar.close()


def traverse(nodeid, folder):
    # 处理文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)
    data = get_nodes(nodeid)
    for item in data:
        if item['kind'] != 'folder':
            download(item['url'], folder + '/' + item['name'])
        else:
            traverse(item['nodeId'], folder + '/' + item['name'])


path = '/pan/api/nodes'
node_id = None
if __name__ == '__main__':
    orgid = personal.get_org_id()
    uid = personal.get_uid()
    spaceid, rootid, base_path = spaces.get_space_id(orgid, uid)
    driveid = devices.get_drive_id(orgid)
    select_folder(rootid)
    node = get_node_detail(node_id)
    # 遍历下载
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if node['kind'] == 'folder':
        traverse(node['nodeId'], base_path)
    else:
        download(node['url'], base_path + '/' + node['name'])
