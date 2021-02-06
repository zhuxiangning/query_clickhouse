#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7

# @Time     : 2021/2/6 13:58
# @Author   : 'Lou Zehua'
# @File     : pre_processors.py

# Notes: Function name can will be called bye eval(). Recommend a name pattern similar to the unit name.
# e.g. 'pre_process_' + UNIT_NAME.replace('-', '_')
def pre_process_test(s, config_obj):
    return {}


def pre_process_action_statistical_characteristics(s, config_obj):
    repo_ids = []
    banned_actor_ids = []
    for it in config_obj.repos:
        repo_ids.append(it.id)
    for it in config_obj.banned_actors:
        repo_ids.append(it.id)
    repo_ids = map(lambda x: str(x), repo_ids)
    banned_actor_ids = map(lambda x: str(x), banned_actor_ids)
    addtional_params = {
        "repo_ids": ','.join(repo_ids),
        "banned_actor_ids": ','.join(banned_actor_ids)
    }
    return addtional_params


def pre_process_activity_repo_top_Chinese(s, config_obj):
    actor_ids = []
    org_ids = []
    repo_ids = []
    for it in config_obj.actors:
        actor_ids.append(it.id)
    for it in config_obj.orgs:
        org_ids.append(it.id)
    for it in config_obj.repos:
        repo_ids.append(it.id)
    actor_ids = map(lambda x: str(x), actor_ids)
    org_ids = map(lambda x: str(x), org_ids)
    repo_ids = map(lambda x: str(x), repo_ids)
    addtional_params = {
        "actor_ids": ','.join(actor_ids),
        "org_ids": ','.join(org_ids),
        "repo_ids": ','.join(repo_ids)
    }
    return addtional_params


def pre_process(func_name, s, config_obj):
    return eval(func_name)(s, config_obj)  # you can define various pre_process functions, and switch them here.
