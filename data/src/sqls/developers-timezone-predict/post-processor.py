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
  d, cur_max_conti_index, max_conti_k_hours = analysis(data)
  # GMT_time_zones = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1]
  GMT_time_zone = cur_max_conti_index if cur_max_conti_index < 12 else (cur_max_conti_index - 24)
  GMT_time_zone = GMT_time_zone - 8
  iframe = """<iframe id="svg" src="{0}?data={1}&GMT_time_zone={2}&max_conti_k_hours={3}"  width="600" height="260"></iframe>""".format('./' + profile.image_svg, json.dumps(d), GMT_time_zone, max_conti_k_hours)
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

    for i in range(0, 24):
        rows = data[data.hour == i]
        if len(rows):
            # prevent zero for min
            c = math.ceil((sum(rows["count"]) - min_count*7) * 10 / ((max_count - min_count)*7))
            d.append(max(1, c))
        else:
            d.append(0)
    k = 12
    d2 = d + d
    cur_max_conti_index = 0
    max_conti_k_hours = d2[cur_max_conti_index]
    for i in range(len(d)):
        temp_sum = sum(d2[i: i+k])
        if max_conti_k_hours < temp_sum:
            max_conti_k_hours = temp_sum
            cur_max_conti_index = i
    return d, cur_max_conti_index, max_conti_k_hours
#}#

show_data_in_browser()
