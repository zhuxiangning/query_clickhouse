#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6

import os
import json
import logging
import logging.config

__author__ = 'Lou Zehua <cs_zhlou@163.com>'
__time__ = '2019/6/16 0016 16:47'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def setup_logging(
        default_path=os.path.join(BASE_DIR, 'etc/logging.json'),
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """
    Setup logging configuration
    You can load your own logging configuration like:
        LOG_CFG=my_new_logging.json python my_server.py
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:  # check if LOG_CFG valid
        path = value
    log_dir = os.path.join(BASE_DIR, 'logs')  # default logs dir
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        f.close()
        handlers = list(config["handlers"].values())
        for handler in handlers:
            if "filename" in handler.keys():
                filename = handler["filename"]
                handler["filename"] = os.path.join(log_dir, filename)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info('Hi, foo')
    try:
        open('/path/does/not/exist', 'rb')
    except (SystemExit, KeyboardInterrupt):
        raise
    except FileNotFoundError as e:
        logger.error('Failed to open file: %s' % e.__str__(), exc_info=True)


if __name__ == '__main__':
    main()
