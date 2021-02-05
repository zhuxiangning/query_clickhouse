#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7

# @Time     : 2021/2/4 16:55
# @Author   : 'Lou Zehua'
# @File     : query_sql.py
import os
import re

import jiphy
import pandas as pd
import numpy as np

from sshtunnel import SSHTunnelForwarder
from clickhouse_driver import Client

from etc import filePathConf, profile
from etc.profile import encoding
from script.utils.fileUtils.create_path import create_dir


class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)


def query_clickhouse(sql):
    with SSHTunnelForwarder(
            (profile.REMOTE_SERVER_IP, profile.REMOTE_SERVER_PORT),
            ssh_username=profile.USERNAME,
            # ssh_pkey=profile.SSH_PRIVATE_KEY,  # private key: alternate verification information
            ssh_password=profile.PASSWORD,
            remote_bind_address=(profile.PRIVATE_SERVER_IP, profile.PRIVATE_SERVER_PORT),
            local_bind_address=('0.0.0.0', 10022)) as tunnel:
        client = Client(host='127.0.0.1', port=tunnel.local_bind_port,
                        user=profile.MYSQL_USERNAME,
                        password=profile.MYSQL_PASSWORD,
                        database=profile.USE_DATABASE)
        rs = client.execute(sql)
        return rs


def braces_exchange(s, temp_ch=('|OB|', '|CB|')):
    s = str(s)
    s = s.replace('{{', temp_ch[0]).replace('}}', temp_ch[1])
    s = s.replace('{', '{{').replace('}', '}}')
    s = s.replace(temp_ch[0], '{').replace(temp_ch[1], '}')
    return s


def sql_standardized(sql, config_obj, braces_ex=True):
    if braces_ex:
        sql = braces_exchange(sql)
    return sql.format_map(config_obj.__dict__)


def pre_process(s):
    return False


def post_process(s, post_process_display_mode):
    ret_heads = None
    if post_process_display_mode == profile.SHOW_TABLE:
        ret_head_def = re.search(r"let ret(\s)*=(\s)*\'.*[.\n]?(\s)*\'(\s)*;(\s)*", s)  # get ret definition line
        ret_head_str = ret_head_def.group(0).split('\'')[1]  # get ret_head
        ret_heads = ret_head_str.replace(' ', '').split('|')[2: -1]
    elif post_process_display_mode == profile.SHOW_SVG:
        # Stage1: create the python file 'post-processor.py' with tool jiphy.
        js_post_processor_path = os.path.join(item_src_dir, profile.post_processor)
        py_post_processor_path = js_post_processor_path.replace('.js', '.py')
        if s and not os.path.exists(py_post_processor_path):
            js_code = s
            raw_py_code = jiphy.to.python(js_code)
            py_templates_svg_code = os.path.join(filePathConf.absPathDict[filePathConf.TEMPLATES_DIR], 'post-processor.svg.py')
            with open(py_templates_svg_code, 'r') as f:
                merged_code = f.read()
            merged_code = re.sub('#{#[\s\S]*#}#', raw_py_code, merged_code)
            with open(py_post_processor_path, 'w') as f:
                f.write(merged_code)
        return None
    else:
        pass
    return ret_heads


def post_process_display_svg(py_post_processor_path, res_csv_save_path, svg_path, prepared=False):
    if prepared:
        os.system('python {0} {1} {2}'.format(py_post_processor_path, res_csv_save_path, svg_path))  # Run the new python script 'post-processor.py' when prepared
    return


if __name__ == '__main__':
    ITEM = 'working-hour-distribution'
    PRE_PROCESSOR = False
    POST_PROCESSOR = True
    POST_PROCESS_DISPLAY_MODE = profile.SHOW_SVG

    item_src_dir = os.path.join(filePathConf.absPathDict[filePathConf.SQLS_DIR], ITEM)
    item_result_dir = item_src_dir.replace('/src/', '/result/')
    create_dir(item_result_dir)

    # if you 'have pre-processor.js', please add pre-process logic here:
    if PRE_PROCESSOR:
        with open(os.path.join(item_src_dir, profile.pre_processor), 'r',
                  encoding=encoding) as f:
            addtional_params = pre_process(f.read())

    with open(os.path.join(item_src_dir, profile.sql), 'r', encoding=encoding) as f:
        sql = f.read()

    with open(os.path.join(item_src_dir, profile.manifest), 'r', encoding=encoding) as f:
        param_dict = eval(f.read())

    # if you 'have post-processor.js', please add post-process logic here:
    if POST_PROCESSOR:
        with open(os.path.join(item_src_dir, profile.post_processor), 'r', encoding=encoding) as f:
            post_processor = f.read()
        ret_heads = post_process(post_processor, POST_PROCESS_DISPLAY_MODE)

    # format sql
    if "table" not in param_dict["config"].keys():
        param_dict["config"]["table"] = profile.tables[profile.WHICH_TABLE]
    param_obj = obj(param_dict)
    config_obj = param_obj.config
    sql = sql_standardized(sql, config_obj)  # format sql string with parameter dict: config_obj

    # query and save to data dir
    rs = query_clickhouse(sql)
    df = pd.DataFrame(np.array(rs), columns=ret_heads)
    df.index = np.arange(1, len(df) + 1)
    res_csv_save_path = os.path.join(item_result_dir, ITEM + '-' + param_dict["config"]["table"] + '.csv')
    df.to_csv(res_csv_save_path)

    if POST_PROCESS_DISPLAY_MODE == profile.SHOW_SVG:
        # Change the python file 'post-processor.py' created by jiphy: function analysis() must be overwrote.
        # post_processor_prepared = False  # Default: False.
        post_processor_prepared = True  # Change it to True after the function analysis() overwritten.
        js_post_processor_path = os.path.join(item_src_dir, profile.post_processor)
        py_post_processor_path = js_post_processor_path.replace('.js', '.py')
        svg_path = os.path.join(item_src_dir, profile.image_svg)
        post_process_display_svg(py_post_processor_path, res_csv_save_path, svg_path, prepared=post_processor_prepared)
