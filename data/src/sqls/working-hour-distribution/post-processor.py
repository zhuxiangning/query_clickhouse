import math
import os
import sys

import pandas as pd
import json
import webbrowser

from etc import profile


def show_data_in_browser():
  py_post_processor_path, res_csv_save_path, svg_html_path = list(sys.argv)[0:3]
  data = pd.read_csv(res_csv_save_path, index_col=0)
  d = analysis(data)
  disp_TZs = [+8, -5]  # display multi-timezones
  iframe = """<iframe src="{0}?data={1}&lang=zh&hide_title=true&hide_lang_btn=true&disp_TZs={2}" width="600" height="260"></iframe>""".format('./' + profile.image_svg, json.dumps(d), json.dumps(disp_TZs))
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
