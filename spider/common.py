# -*- coding: utf-8
import sys
import logging
import os
from config import *

def set_log(level, filename='spider.log'):
    """
    return a log file object
    根据提示设置log打印
    """
    if not os.path.isdir(LOG_DIR):
    	os.mkdir(LOG_DIR)
    log_file = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(log_file):
        os.mknod(log_file)
        os.chmod(log_file, 0777)
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}
    logger_f = logging.getLogger('spider')
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file,'a')
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s  %(filename)s  [line:%(lineno)d] %(levelname)s  %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    keep_fds = [fh.stream.fileno()]
    return logger_f,keep_fds


logger,keep_fds=set_log(LOG_LEVEL)
