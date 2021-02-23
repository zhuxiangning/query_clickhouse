#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7

# @Time     : 2021/2/22 20:24
# @Author   : 'Lou Zehua'
# @File     : routes.py
import json
import math
import os
import sys

from flask import render_template, request
from markupsafe import Markup

from app import app
import pandas as pd

from etc import filePathConf


@app.route('/')
@app.route('/index', methods=['get', 'post'])
def index():
    params = {
        "src": None,
        "data": None,
        "lang": "zh",
        "hide_title": "true",
        "hide_lang_btn": "true",
        "disp_TZs": [0, +8, -5],  # display multi-timezones
    }
    base_uri = '.'
    params.update(request.form.to_dict())
    params.update(request.args.to_dict())
    # py_show_svg_path, res_csv_save_path, svg_html_path = """E:\git_repo\query_clickhouse\data\src\sqls\working-hour-distribution\post-processor.py E:\git_repo\query_clickhouse\data\\result\sqls\working-hour-distribution\working-hour-distribution-github_log.year2020.csv E:\git_repo\query_clickhouse\data\src\sqls\working-hour-distribution\image.svg-github_log.year2020.html""".split(' ')
    py_show_svg_path, res_csv_save_path, svg_html_path = list(sys.argv)[0:3]
    data = pd.read_csv(res_csv_save_path, index_col=0)
    data = analysis(data)
    params["src"] = os.path.join(os.path.dirname(res_csv_save_path).replace(filePathConf.BASE_DIR, base_uri).replace('\\', '/').replace('/result/', '/src/'), 'image.svg')
    params["data"] = json.dumps(data)
    iframe = """<iframe src="{src}?data={data}&lang={lang}&hide_title={hide_title}&hide_lang_btn={hide_lang_btn}&disp_TZs={disp_TZs}" width="650" height="250"></iframe>""".format(**params)
    return render_template("index.html", iframe=Markup(iframe))



# # Update your code when you change to a new task!
# def analysis(data):
#     pass
#{#
def analysis(data):
    data = pd.DataFrame(data)
    data.columns = ["count", "dayOfWeek", "hour"]
    min_count = min(data["count"])
    max_count = max(data["count"])
    d = []
    for j in range(1, 7 + 1):
        for i in range(0, 24):
            rows = data[(data.dayOfWeek == j) & (data.hour == i)]
            if len(rows):
                # prevent zero for min
                c = math.ceil((rows["count"] - min_count) * 10 / (max_count - min_count))
                d.append(max(1, c))
            else:
                d.append(0)
    return d
#}#


app.run("127.0.0.1", 5000, debug=True)
