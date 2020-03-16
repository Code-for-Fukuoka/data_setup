#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Usage: merge_json.py

"""
    福："contacts"
    福："querents"
    福："patients"
　　福："patients_summary"
　　仮："discharges_summary"
　　福："inspections"
　　福："inspections_summary"
　　仮："better_patients_summary"
　　福："lastUpdate"
　　仮："main_summary"
"""

""" libs
"""
import configparser
import os
import pandas as pd
import csv
import json
import pprint
import datetime

def output_json(o_file_name, o_list):

    if DEBUG == 0:
    
        o_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + o_file_name
    
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
            f_filename = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + data_name + ".json"

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

    WORK_DIR = config.get(config_section, 'WORK_DIR')
    INPUT_DIR = config.get(config_section, 'INPUT_DIR')
    OUTPUT_DIR = config.get(config_section, 'OUTPUT_DIR')
    TOOL_DIR = config.get(config_section, 'TOOL_DIR')
    RESOURCE_FILE = config.get(config_section, 'RESOURCE_FILE')
    
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
        "lastUpdate",
        "main_summary"
        ]
    
    main()
