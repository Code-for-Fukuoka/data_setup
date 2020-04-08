#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Usage: gen_json.py

""" libs
"""
import configparser
import os
import pandas as pd
import csv
import json
import pprint
import datetime
import urllib.error
import urllib.parse
import urllib.request
import http.client
import requests
import io
import chardet
from datetime import datetime as dt

""" defs
"""
def get_resource_file_dict(resource_file_dict_file):
    
    with open(resource_file_dict_file) as f:
        resource_file_dict = json.load(f)
        f.close()

    return(resource_file_dict)

def call_api(request_url):

    response_dict = None
    request = urllib.request.Request(request_url)

    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            response_page = response.read()

    except urllib.error.HTTPError as e:
        w = 'HTTPError'
        print("%12s %s %s" % (w, e.code, request_url))
        pass

    except urllib.error.URLError as e:
        w = 'URLError'
        print("%12s %s %s" % (w, e.code, request_url))
        pass

    except http.client.BadStatusLine as e:
        w = 'BadStatusError'
        print("%12s %s %s" % (w, e.code, request_url))
        pass

    else:
        response_dict = json.loads(response_page)

    return(response_dict)


def get_package_data():

    ckan_dict = {}
    resource_dict = {}
    
    for f_title in DATA_DICT['resource']:
        type = DATA_DICT['resource'][f_title]['type']
        use = DATA_DICT['resource'][f_title]['use']
        dataset = DATA_DICT['resource'][f_title]['dataset']

        api_com = 'package_show' + '?id=' + dataset
        url = BASE_URL + '/api/3/action/' + api_com

        if type == "url" and use == 'True':
            resp_dict = call_api(url)
            ckan_dict[f_title] = resp_dict
            resource_dict[f_title] = resp_dict['result']

    return(resource_dict)


def conv_time(package_date):

    pd = package_date.split('.')

    td = dt.strptime(pd[0], '%Y-%m-%dT%H:%M:%S')
    td_jpn = td + datetime.timedelta(hours=9)
    td_jpn_str = td_jpn.strftime('%Y-%m-%dT%H:%M:%S')
    
    td_jpn_str_sep = td_jpn_str.split('T')
    td_date = td_jpn_str_sep[0]
    td_time = td_jpn_str_sep[1]
    
    hour = td_time.split(':')[0]
    min  = td_time.split(':')[1]
    sec  = td_time.split(':')[2]

    datetime_str = td_date + " " + hour + ":" + min
    
    return(datetime_str)

def show_package_info(resource_dict):

    for f_title in DATA_DICT['resource']:
        format = DATA_DICT['resource'][f_title]['type']
        use = DATA_DICT['resource'][f_title]['use']

        if format == "url" and use == 'True':
            last_modified = resource_dict[f_title]["resources"][0]["last_modified"]

            last_modified_jpn = conv_time(last_modified)
            
            dateandtime = last_modified_jpn.replace('T', ' ')
            
            print("{0:12s} : {1}".format(f_title, dateandtime))

    return()

def main():

    # パッケージのメタデータを取得
    resource_dict = get_package_data()

    show_package_info(resource_dict)

if __name__ == '__main__':

    config = configparser.ConfigParser()
    path = os.getcwd()
    config.read('{}/../config.ini'.format(path), encoding="utf-8")
    config_section = 'development'

    WORK_DIR = os.path.dirname(os.path.abspath(__file__))
    WORK_DIR = os.path.dirname(WORK_DIR)
    TOOL_DIR = os.path.basename(WORK_DIR)
    WORK_DIR = os.path.dirname(WORK_DIR)

    INPUT_DIR = config.get(config_section, 'INPUT_DIR')
    OUTPUT_DIR = config.get(config_section, 'OUTPUT_DIR')
    RESOURCE_FILE = config.get(config_section, 'RESOURCE_FILE')
    
    DEBUG = 1

    """
    hotline: 新型コロナコールセンター相談件数
    visit: 新型コロナ受診相談件数
    inspections: 検査実施数
    patients: 福岡市新型コロナ陽性患者発表情報
    """

    resource_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + RESOURCE_FILE
    DATA_DICT = get_resource_file_dict(resource_file_path)

    BASE_URL = DATA_DICT['organization']['url']
    
    main()
