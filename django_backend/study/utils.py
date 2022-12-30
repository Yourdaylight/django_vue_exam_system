# -*- coding: utf-8 -*-
# @Time    :2022/12/25 16:03
# @Author  :lzh
# @File    : utils.py
# @Software: PyCharm
import os
import json


# 传入一个树状结构的json，返回一个列表
def get_list_from_tree(tree):
    res = []
    # 深拷贝tree
    _tree = json.loads(json.dumps(tree))
    for item in _tree:
        if item.get("children"):
            children = item.pop("children")
            res.append(item)
            res.extend(get_list_from_tree(children))
        else:
            res.append(item)
    return res


# 传入一个树状结构的json，传入要查询的id,传入要修改的key和value，返回修改后的树状结构
def update_tree(tree, _id, key, value):
    for item in tree:
        if item.get("id") == _id:
            item[key] = value
        if item.get("children"):
            update_tree(item.get("children"), _id, key, value)
    return tree


# 将数组结构json写入本地文件
def write_json_to_file(json_data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(json_data))


if __name__ == '__main__':
    with open("content.json", encoding="utf-8") as f:
        content = json.load(f)
        print(update_tree(content, 1, "label", "lzh"))
