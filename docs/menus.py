#!usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
import os
from pathlib import Path
import json
import platform
from flask_cors import *

app = Flask(__name__)  # 创建应用实例


@app.route('/config')  # route装饰器创建路由
@cross_origin(supports_credentials=True)
def config():  # 访问此路由时执行的视图函数
    root = replace_windows(os.getcwd())
    # root = r"D:/Soft/nginx-1.20.2/dist"
    print(root)
    path = os.path.join(root, "static")
    res = bianli_dir(path, 1)
    print(res)
    json_res = json.dumps(res, indent=2, ensure_ascii=False)
    return """{"title": "学习笔记",
       "topicWidth": 250,
       "openLevel": 0,
       "topics": """ + json_res.replace(root, '').replace(r'\\', '/') + "}"


def bianli_dir(dir, i):
    i = i + 1
    p = Path(dir)
    DirTree = []
    # print(p)
    for p in list(p.glob('*')):
        if p.is_file() and (p.name.endswith(".md")):
            # print(p.name)
            DirTree.append({"id": i, "name": p.name.replace(".md", ""), "src": os.path.join(dir, p.name)})
        elif p.is_dir():
            j = i * 100
            subdir = bianli_dir(os.path.join(dir, p.name), j);
            DirTree.append({"id": j, "name": p.name.replace(".md", ""), "submenus": subdir})
        i = i + 1
    return DirTree


def replace_windows(str):
    if platform.system() == 'Windows':
        return str.replace('\\', '/')
    else:
        return str


if __name__ == '__main__':
    # app.run(debug=True)  # 开始运行flask应用程序，以调试模式运行
    # 可以设置启动的host地址和端口号，具体方法：
    # CORS(app, supports_credentials=True)
    app.run(host='localhost', port=3243)
