import copy
import math
import os
import sys

import numpy as np
import pandas as pd
import json
import webbrowser

from etc import profile

CONTI_K_HOURS = 12
GMT = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1]
KEEP_ORIGIN = False
UPDATE_REL_RESULT_CSV = False


def show_data_in_browser():
    py_post_processor_path, res_csv_save_path, svg_html_path = list(sys.argv)[0:3]
    rel_res_csv_save_path = res_csv_save_path.replace(".csv", ".rel-result.csv")
    if os.path.isfile(rel_res_csv_save_path) and not UPDATE_REL_RESULT_CSV:
        df = pd.read_csv(rel_res_csv_save_path, index_col=0)
        actor_ids, GMT_time_zones, actor_24hours_list = df['actor_id'].values, df['time_zone'].values, df[list(map(str, list(range(24))))].values
        max_conti_k_hours_list = np.zeros(len(actor_ids))
    else:
        data = pd.read_csv(res_csv_save_path, index_col=0)
        actor_ids, actor_max_conti_indexes, max_conti_k_hours_list, actor_24hours_list = analysis(data)
        GMT_time_zones = []
        actor_rel_24hours_list = copy.deepcopy(actor_24hours_list) if KEEP_ORIGIN else actor_24hours_list
        for i in range(len(actor_max_conti_indexes)):
            time_diff = actor_max_conti_indexes[i] - 8
            if time_diff != 0:
                actor_rel_24hours_list[i] = actor_rel_24hours_list[i][time_diff:] + actor_rel_24hours_list[i][:time_diff]
        df_actor_rel_24hours_lists = pd.DataFrame(np.array(actor_rel_24hours_list))

        for i in range(len(actor_ids)):
            GMT_time_zone = actor_max_conti_indexes[i] if actor_max_conti_indexes[i] < 12 else (actor_max_conti_indexes[i] - 24)
            GMT_time_zone = GMT[GMT_time_zone - 8]
            GMT_time_zones.append(GMT_time_zone)
        df = pd.DataFrame({"actor_id": actor_ids, "time_zone": GMT_time_zones})
        df = pd.concat([df, df_actor_rel_24hours_lists], axis=1)
        df_stat = pd.DataFrame({"actor_id": [-1, -2, -3, -4], "time_zone": [0, 0, 0, 0]})
        df_stat_actor_rel_24hours_lists = pd.DataFrame([df_actor_rel_24hours_lists.sum(axis=0), df_actor_rel_24hours_lists.max(axis=0), df_actor_rel_24hours_lists.mean(axis=0), df_actor_rel_24hours_lists.min(axis=0)])
        df_stat = pd.concat([df_stat, df_stat_actor_rel_24hours_lists], axis=1)
        df_stat.index = ['sum', 'max', 'mean', 'min']
        df = df_stat.append(df)
        df.to_csv(rel_res_csv_save_path)

    example_idx = 2
    max_each_hour = max(np.array(actor_24hours_list[1]))
    d = np.array(actor_24hours_list[example_idx])
    d = d * 10 / max_each_hour
    GMT_time_zone = GMT_time_zones[example_idx]
    max_conti_k_hours = max_conti_k_hours_list[example_idx]
    iframe = """<iframe id="svg" src="{0}?data={1}&GMT_time_zone={2}&max_conti_k_hours={3}"  width="600" height="260"></iframe>""".format('./' + profile.image_svg, json.dumps(list(d)), GMT_time_zone, max_conti_k_hours)
    with open(svg_html_path, 'w') as f:
        f.write(iframe)
    webbrowser.open_new_tab(svg_html_path)


# # Update your code when you change to a new task!
# def analysis(data):
#     pass
#{#
def analysis(data):
    data = pd.DataFrame(data)
    data.columns = ["actor_id", "hour", "count"]
    min_count = min(data["count"])
    max_count = max(data["count"])
    actor_ids = []
    actor_max_conti_index = []
    max_conti_k_hours_list = []
    actor_24hours = []

    for actor_id, single_actor_data in data.groupby(data["actor_id"]):
        d = []
        for i in range(0, 24):
            rows = single_actor_data[single_actor_data.hour == i]
            if len(rows):
                # prevent zero for min
                c = math.ceil((sum(rows["count"]) - min_count*7) * 10 / ((max_count - min_count)*7))
                d.append(max(1, c))
            else:
                d.append(0)
        k = CONTI_K_HOURS
        d2 = d + d
        cur_max_conti_index = 0
        max_conti_k_hours = d2[cur_max_conti_index]
        for i in range(len(d)):
            temp_sum = sum(d2[i: i+k])
            if max_conti_k_hours < temp_sum:
                max_conti_k_hours = temp_sum
                cur_max_conti_index = i
        actor_ids.append(actor_id)
        actor_max_conti_index.append(cur_max_conti_index)
        max_conti_k_hours_list.append(max_conti_k_hours)
        actor_24hours.append(d)
    return actor_ids, actor_max_conti_index, max_conti_k_hours_list, actor_24hours
#}#

show_data_in_browser()
