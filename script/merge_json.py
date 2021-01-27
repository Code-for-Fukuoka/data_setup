#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Usage: merge_json.py

""" libs
"""
import configparser
import os
import pandas as pd
import csv
import json
import pprint
import datetime

def load_json_file(json_filename):
    
    with open(json_filename) as f:
        dict = json.load(f)
        f.close()

    return(dict)
                
def output_json(o_file_name, o_list):

    if DEBUG == 0:
    
        o_file_path = O_FILEPATH + "/" + o_file_name
    
        f = open(o_file_path, 'w')
        json.dump(o_list, f, indent=4, ensure_ascii=False)
    
    return()

""" defs
"""
def main():

    now = datetime.datetime.now()
    now_date = now.strftime('%Y/%m/%d %H:%M')
    now_date = now_date.replace('/', '\/')

    dict_all = {}
    
    for data_name in DATA_LIST:

        print("merge:", data_name)
        
        if data_name == "lastUpdate":
            dict = {"lastUpdate":now_date}
            dict_all.update(dict)
            
        else:
            org_data_filename = ORG_ID + "_" + data_name + ".json"
            f_filename = O_FILEPATH + "/" + org_data_filename

            with open(f_filename) as f:
                dict = json.load(f)
            """
            pprint.pprint(dict)
            """
            dict_all.update(dict)
            
    # pprint.pprint(dict_all)
    output_json("data_new.json", dict_all)
    
    return
                
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

    I_FILEPATH = WORK_DIR + "/" + TOOL_DIR + "/" + INPUT_DIR
    O_FILEPATH = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR

    resource_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + RESOURCE_FILE
    DATA_DICT = load_json_file(resource_file_path)
    
    ORG_ID = DATA_DICT['organization']['id']
    
    DEBUG = 0

    DATA_LIST = [
        "tested",
        "contacts",
        "querents",
        "patients",
        "patients_summary",
        "discharges_summary",
        "inspections",
        "inspections_summary",
        "better_patients_summary",
        "patients_status_daily",
        "lastUpdate",
        "main_summary"
        ]
    
    main()
