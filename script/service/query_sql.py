#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7

# @Time     : 2021/2/4 16:55
# @Author   : 'Lou Zehua'
# @File     : query_sql.py
import json
import logging
import os
import re
import sys
import traceback

import jiphy
import pandas as pd
import numpy as np

from sshtunnel import SSHTunnelForwarder
from clickhouse_driver import Client

from etc import filePathConf, profile
from etc.profile import encoding
from script.service.pre_processors import pre_process
from script.utils.fileUtils.create_path import create_dir

logger = logging.getLogger(__name__)


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


def sql_standardized(sql, config_obj, braces_exch=True):
    if braces_exch:
        sql = braces_exchange(sql)
    try:
        sql = sql.format_map(config_obj.__dict__)
        sql = re.sub('\[\[(.*)\]\]', r'[\1]', sql)  # when format list string, replace '[[]]' with '[]'
        sql = re.sub('\{\{(.*)\}\}', r'{\1}', sql)  # when format dict string, replace '{{}}' with '{}'
    except BaseException as e:
        logger.error('Check whether the function "pre_processor" works well.\n' + traceback.format_exc())
        sys.exit()
    return sql


def post_process(s, post_process_display_mode):
    ret_heads = None
    if post_process_display_mode == profile.SHOW_TABLE:
        ret_head_def = re.search(r"let ret(\s)*=(\s)*\'.*[.\n]?(\s)*\'(\s)*;(\s)*", s)  # get ret definition line
        if ret_head_def:
            ret_head_str = ret_head_def.group(0).split('\'')[1]  # get ret_head
            ret_heads = ret_head_str.replace(' ', '').split('|')[2: -1]
    elif post_process_display_mode == profile.SHOW_SVG:
        # create the python file 'post-processor.py' with tool jiphy.
        js_post_processor_path = os.path.join(units_src_dir, profile.post_processor)
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


def post_process_display_svg(py_post_processor_path, res_csv_save_path, svg_html_path, prepared=False):
    if prepared:
        os.system('python {0} {1} {2}'.format(py_post_processor_path, res_csv_save_path, svg_html_path))  # Run the new python script 'post-processor.py' when prepared
    return


def auto_update_sqls_brief(json_path, update):
    if not update:
        return
    sqls = []
    sqls_groups = []
    for root, dirs, files in os.walk(filePathConf.absPathDict[filePathConf.SRC_DIR]):
        if root.endswith('/sqls') or root.endswith('\\sqls'):
            sqls_groups.append((root, dirs))
    for root, dirs in sqls_groups:
        root = root.replace(filePathConf.BASE_DIR, '.')
        root = root.replace('\\', '/')
        root = root + '/'
        func_units = []
        for each_dir in dirs:
            current_rel_dir = os.path.join(root, each_dir)
            current_dir = current_rel_dir.replace('.', filePathConf.BASE_DIR)
            post_process_display_mode = 0  # default mode: SHOW_TABLE
            file_names = os.listdir(current_dir)
            file_exts = []
            for file_name in file_names:
                file_exts.append(os.path.splitext(file_name)[-1])
            if '.svg' in file_exts:
                post_process_display_mode = 1
            func_unit = {
                    "unit_name": each_dir,
                    "pre_processor": os.path.exists(os.path.join(current_dir, profile.pre_processor)),
                    "post_processor": os.path.exists(os.path.join(current_dir, profile.post_processor)),
                    "post_process_display_mode": post_process_display_mode
                }
            func_units.append(func_unit)
        sqls_dscp_func_units = {
                "relative_dir": root,
                "func_units": func_units,
            }
        sqls.append(sqls_dscp_func_units)
    description = "Auto generated briefs according to files in the corresponding directory 'sqls/'."
    sqls_brief = {
        "sqls": sqls,
        "description": description
    }
    with open(json_path, 'w') as f:
        json.dump(sqls_brief, f, indent=2)
    return


if __name__ == '__main__':
    UPDATE_SQLS_BRIEF = True
    WHICH_TABLE_NAME = profile.tables[profile.WHICH_TABLE + 0]
    WHICH_SQLS_GROUP = 1  # index start from 0
    WHICH_FUNC_UNITS = 2  # index start from 0

    json_path = filePathConf.absPathDict[filePathConf.BRIEF_SQLS_PATH]
    auto_update_sqls_brief(json_path, UPDATE_SQLS_BRIEF)
    with open(json_path, 'r') as f:
        sqls_brief_load = json.load(f)
    units_relative_dir = sqls_brief_load["sqls"][WHICH_SQLS_GROUP]["relative_dir"]
    brief_func_units = sqls_brief_load["sqls"][WHICH_SQLS_GROUP]["func_units"][WHICH_FUNC_UNITS]
    UNIT_NAME = brief_func_units["unit_name"]
    PRE_PROCESSOR = brief_func_units["pre_processor"]
    POST_PROCESSOR = brief_func_units["post_processor"]
    POST_PROCESS_DISPLAY_MODE = brief_func_units["post_process_display_mode"]

    units_src_dir = os.path.join(units_relative_dir.replace('.', filePathConf.BASE_DIR), UNIT_NAME)
    print('units_src_dir:', units_src_dir)
    item_result_dir = units_src_dir.replace('/src/', '/result/')
    create_dir(item_result_dir)

    with open(os.path.join(units_src_dir, profile.sql), 'r', encoding=encoding) as f:
        sql = f.read()

    with open(os.path.join(units_src_dir, profile.manifest), 'r', encoding=encoding) as f:
        param_dict = eval(f.read())

    if "table" not in param_dict["config"].keys():
        param_dict["config"]["table"] = WHICH_TABLE_NAME
    param_obj = obj(param_dict)
    config_obj = param_obj.config

    # if you 'have pre-processor.js', please add pre-process logic here:
    if PRE_PROCESSOR:
        with open(os.path.join(units_src_dir, profile.pre_processor), 'r',
                  encoding=encoding) as f:
            # update the suffix when a new pre_process function is defined in 'pre_processors.py'
            # Notes: Recommend a name pattern similar to the unit name. e.g. UNIT_NAME.replace('-', '_')
            PRE_PROCESS_FUNC_SUFFIX = UNIT_NAME.replace('-', '_')
            addtional_params = pre_process('pre_process_' + PRE_PROCESS_FUNC_SUFFIX, f.read(), config_obj)
            config_obj.__dict__ = dict(config_obj.__dict__, **addtional_params)


    # if you 'have post-processor.js', please add post-process logic here:
    if POST_PROCESSOR:
        with open(os.path.join(units_src_dir, profile.post_processor), 'r', encoding=encoding) as f:
            post_processor = f.read()
        ret_heads = post_process(post_processor, POST_PROCESS_DISPLAY_MODE)

    # format sql
    sql = sql_standardized(sql, config_obj)  # format sql string with parameter dict: config_obj

    # query and save to data dir
    rs = query_clickhouse(sql)
    df = pd.DataFrame(np.array(rs), columns=ret_heads)
    df.index = np.arange(1, len(df) + 1)
    res_csv_save_path = os.path.join(item_result_dir, UNIT_NAME + '-' + param_dict["config"]["table"] + '.csv')
    df.to_csv(res_csv_save_path)

    if POST_PROCESS_DISPLAY_MODE == profile.SHOW_SVG:
        # Change the python file 'post-processor.py' created by jiphy: function analysis() must be overwrote.
        # post_processor_prepared = False  # Default: False.
        post_processor_prepared = True  # Change it to True after the function analysis() overwritten.
        js_post_processor_path = os.path.join(units_src_dir, profile.post_processor)
        py_post_processor_path = js_post_processor_path.replace('.js', '.py')
        svg_path = os.path.join(units_src_dir, profile.image_svg)
        svg_html_path = svg_path + '-' + param_dict["config"]["table"] + '.html'
        post_process_display_svg(py_post_processor_path, res_csv_save_path, svg_html_path, prepared=post_processor_prepared)
