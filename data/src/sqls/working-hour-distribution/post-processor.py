import math
import os
import sys

import pandas as pd
import json
import webbrowser

from etc import filePathConf

def show_data_in_browser():
    params = {
        "src": None,
        "data": None,
        "lang": "zh",
        "hide_title": "true",
        "hide_lang_btn": "true",
        "disp_TZs": [0, +8, -5],  # display multi-timezones
    }
    base_uri = filePathConf.BASE_DIR
    py_post_processor_path, res_csv_save_path, svg_html_path = list(sys.argv)[0:3]
    data = pd.read_csv(res_csv_save_path, index_col=0)
    data = analysis(data)
    params["src"] = os.path.join(os.path.dirname(res_csv_save_path).replace(filePathConf.BASE_DIR, base_uri).replace('\\', '/').replace('/result/', '/src/'), 'image.svg')
    params["data"] = json.dumps(data)
    iframe = """<iframe src="{src}?data={data}&lang={lang}&hide_title={hide_title}&hide_lang_btn={hide_lang_btn}&disp_TZs={disp_TZs}" width="650" height="260"></iframe>""".format(**params)
    with open(svg_html_path, 'w') as f:
        f.write(iframe)
    webbrowser.open_new_tab(svg_html_path)


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

show_data_in_browser()
