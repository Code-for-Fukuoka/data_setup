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
def load_json_file(json_filename):
    
    with open(json_filename) as f:
        dict = json.load(f)
        f.close()

    return(dict)
                
def get_datetime(date):
    pdate = datetime.datetime.strptime(date, '%Y/%m/%d').strftime('%Y-%m-%d %H:%M:%S')
    date = pdate.split(' ')[0]
    time = pdate.split(' ')[1]
    return(date, time)

def get_numofweek(dayofweek):

    if   dayofweek == '月':
        w = 1
    elif dayofweek == '火':
        w = 2
    elif dayofweek == '水':
        w = 3
    elif dayofweek == '木':
        w = 4
    elif dayofweek == '金':
        w = 5
    elif dayofweek == '土':
        w = 6
    elif dayofweek == '日':
        w = 7
    else:
        print("DayofWeek is wrong", dayofweek)
        exit()

    return(w)

def get_shortdate(date):

    date_list = date.split("-")

    month = date_list[1]
    day   = date_list[2]

    short_date = month + r'\/' + day

    return(short_date)

def conv_hotline(records_dict):

    records_list = []
    
    for record in records_dict:
        date = record['年月日']
        dayofweek = record['曜日']
        num = int(float(record['件数']))

        # make Number of Week
        numofweek = get_numofweek(dayofweek)
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'
        # make short date
        shortdate = get_shortdate(date)
        
        record_dict= {}
        record_dict["日付"] = dateandtime
        record_dict["曜日"] = dayofweek
        record_dict["9-13時"] = 0
        record_dict["13-17時"] = 0
        record_dict["17-21時"] = num
        record_dict["date"] = date
        record_dict["w"] = numofweek
        record_dict["short_date"] = shortdate
        record_dict["小計"] = num

        records_list.append(record_dict)

    return(records_list)

def conv_visit(records_dict):

    records_list = []
    
    for record in records_dict:
        date = record['年月日']
        dayofweek = record['曜日']
        num = int(float(record['件数']))

        # make Number of Week
        numofweek = get_numofweek(dayofweek)
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'
        # make short date
        shortdate = get_shortdate(date)
        
        record_dict= {}
        record_dict["日付"] = dateandtime
        record_dict["曜日"] = dayofweek
        record_dict["9-17時"] = num
        record_dict["17-翌9時"] = 0
        record_dict["date"] = date
        record_dict["w"] = numofweek
        record_dict["short_date"] = shortdate
        record_dict["小計"] = num

        records_list.append(record_dict)
    
    return(records_list)

def conv_inspections(records_dict):

    records_list = []
    
    for record in records_dict:
        date = record['年月日']
        dayofweek = record['曜日']
        num = int(float(record['件数']))

        # make Number of Week
        numofweek = get_numofweek(dayofweek)
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'

        date_list = date.split('-')
        inspection_date = date_list[1] + r'\/' + date_list[2] + r'\/' + date_list[0]

        record_dict= {}
        record_dict["判明日"] = inspection_date
        record_dict["検査検体数"] = str(num)
        record_dict["疑い例検査"] = "0"
        record_dict["接触者調査"] = "0"
        record_dict["陰性確認"] = "0"
        record_dict["（小計①）"] =str(num)
        record_dict["チャーター便"] = "0"
        record_dict["クルーズ船"] = "0"
        record_dict["陰性確認2"] = "0"
        record_dict["（小計②）"] =" 0"

        records_list.append(record_dict)
    
    return(records_list)

def conv_tested(records_dict):

    records_list = []
    
    for record in records_dict:
        date = record['年月日']
        dayofweek = record['曜日']
        num = int(float(record['件数']))

        # make Number of Week
        numofweek = get_numofweek(dayofweek)
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'
        # make short date
        shortdate = get_shortdate(date)

        date_list = date.split('-')
        inspection_date = date_list[1] + r'\/' + date_list[2] + r'\/' + date_list[0]

        record_dict= {}
        record_dict["日付"] = dateandtime
        record_dict["曜日"] = dayofweek
        record_dict["件数"] = num
        record_dict["date"] = date
        record_dict["w"] = numofweek
        record_dict["short_date"] = date
        record_dict["小計"] = num
        
        records_list.append(record_dict)
    
    return(records_list)

def conv_patients(records_dict):
    
    records_list = []
    
    for record in records_dict:
        date = record['公表_年月日']
        dayofweek = record['曜日']
        residence = record['居住地']
        age = record['年代']
        sex = record['性別']
        if record['退院済フラグ'] == 1:
            discharge = '○'
        else: 
            discharge = ''
           

        # make Number of Week
        numofweek = get_numofweek(dayofweek)
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'

        record_dict= {}
        record_dict["リリース日"] = dateandtime
        record_dict["曜日"] = 0
        record_dict["居住地"] = residence
        record_dict["年代"] = age
        record_dict["性別"] = sex
        record_dict["退院"] = discharge
        record_dict["date"] = date 

        records_list.append(record_dict)
    
    return(records_list)

def conv_better_patients_summary_dict(records_dict, f_title):

    better_record_dict= {}
    
    for record in records_dict:
        date = record['年月日']
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'

        if f_title == "patients":
            num = record['患者判明数']
        elif f_title == "discharge":
            num = record['退院者数']
        elif f_title == "died":
            num = record['死亡者数']
        elif f_title == "mild":
            num = record['軽症']
        elif f_title == "medium":
            num = record['中等症']
        elif f_title == "heavy":
            num = record['重症']
        else:
            print("wrong f_title:", f_title)
            exit()

        better_record_dict[dateandtime] = int(num)
        
    return(better_record_dict)

def conv_patients_summary_list(records_dict, f_title):

    records_list = []
    
    for record in records_dict:
        date = record['年月日']
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'

        if f_title == "patients":
            num = record['患者判明数']
        elif f_title == "discharge":
            num = record['退院者数']
        elif f_title == "died":
            num = record['死亡者数']
        elif f_title == "mild":
            num = record['軽症']
        elif f_title == "medium":
            num = record['中等症']
        elif f_title == "heavy":
            num = record['重症']
        else:
            print("wrong f_title:", f_title)
            exit()

        record_dict= {}
        record_dict["日付"] = dateandtime
        record_dict["小計"] = int(num)
        records_list.append(record_dict)
        
    return(records_list)

def gen_main_summary(total_visit,
                     total_patients,
                     total_discharge,
                     total_inspections,
                     total_died,
                     total_mild,
                     total_medium,
                     total_heavy):

    main_summary_dict = {
        "main_summary": {
            "attr": "検査実施人数",
            "value": total_inspections,
            "children": [
                {
                    "attr": "陽性患者数",
                    "value": total_patients,
                    "children": [
                        {
                            "attr": "入院中",
                            "value": total_patients - total_discharge,
                            "children": [
                                {
                                    "attr": "軽症・中等症",
                                    "value": total_mild + total_medium
                                },
                                {
                                    "attr": "重症",
                                    "value": total_heavy
                                }
                            ]
                        },
                        {
                            "attr": "退院",
                            "value": total_discharge
                        },
                        {
                            "attr": "死亡",
                            "value": total_died
                        }
                    ]
                }
            ]
        }
    }

    filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "main_summary.json"
    output_json(filepath, main_summary_dict)
    
    return()

def get_date_label(date):

    date_list = date.split('/')

    month = date_list[1]
    day = date_list[2]

    date_label = day + '\/' + month
    
    return(date_label)

def conv_inspections_summary(records_dict):

    city_list = []
    others_list = []
    label_list = []

    for record in records_dict:
        num = int(float(record['件数']))
        date = record['年月日']
        date_label = get_date_label(date)

        city_list.append(num)
        others_list.append(0)
        label_list.append(date_label)

    inspections_summary_dict = {
        "市内": city_list,
        "その他": others_list
    }
    
    return(inspections_summary_dict, label_list)

def output_json(o_filepath, o_dict):

    f = open(o_filepath, 'w')
    json.dump(o_dict, f, indent=4, ensure_ascii=False)
    
    return()

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

    datetime_str = td_date.replace('-', '\/') + " " + hour + ":" + min
    
    return(datetime_str)

def main_sub():

    now = datetime.datetime.now()
    now_date = now.strftime('%Y/%m/%d %H:%M')
    now_date = now_date.replace('/', r'\/')

    for f_title in DATA_DICT:
        
        file_name = DATA_DICT[f_title]["filename"]
        file_path = WORK_DIR + "/" + TOOL_DIR + "/" + INPUT_DIR + "/" + file_name

        print("load:", file_name)
        
        df = pd.read_csv(file_path)
        
        if f_title == "hotline":
            
            df_fill = df.fillna({'件数':0})
            records_dict = df_fill.to_dict(orient='records')
            hotline_list = conv_hotline(records_dict)

            hotline_date = PACKAGE_DICT["hotline"]["resources"][0]["last_modified"]
            hotline_date_str = conv_time(hotline_date)
            
            hotline_dict = {
                "contacts" : {
                    "date" : hotline_date_str,
                    "data" : hotline_list
                }
            }

            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "contacts.json"
            output_json(filepath, hotline_dict)
            
        elif f_title == "visit":
            
            df_fill = df.fillna({'件数':0})
            records_dict = df_fill.to_dict(orient='records')
            visit_list = conv_visit(records_dict)

            visit_date = PACKAGE_DICT["visit"]["resources"][0]["last_modified"]
            visit_date_str = conv_time(visit_date)
            
            visit_dict = {
                "querents": {                
                    "date" : visit_date_str,
                    "data" : visit_list
                }
            }
            
            total_visit = 0
            for d in visit_list:
                total_visit = total_visit + int(d['小計'])
            
            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "querents.json"
            output_json(filepath, visit_dict)

        elif f_title == "patients":
            
            df_fill = df.fillna({'退院済フラグ':0})
            records_dict = df_fill.to_dict(orient='records')
            patients_list = conv_patients(records_dict)

            patients_date = PACKAGE_DICT["patients"]["resources"][0]["last_modified"]
            patients_date_str = conv_time(patients_date)
            
            patients_dict = {
                "patients": {                
                    "date" : patients_date_str,
                    "data" : patients_list
                }
            }
            
            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "patients.json"
            output_json(filepath, patients_dict)

        elif f_title == "inspections":
            
            df_fill = df.fillna({'件数':0})
            records_dict = df_fill.to_dict(orient='records')
            inspections_list = conv_inspections(records_dict)
            tested_list = conv_tested(records_dict)

            inspections_date = PACKAGE_DICT["inspections"]["resources"][0]["last_modified"]
            inspections_date_str = conv_time(inspections_date)
            
            inspections_dict = {
                "inspections": {                
                    "date" : inspections_date_str,
                    "data" : inspections_list
                }
            }

            tested_dict =  {
                "tested": {
                    "date" : inspections_date_str,
                    "data" : tested_list
                }
            }
            
            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "inspections.json"
            output_json(filepath, inspections_dict)

            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "tested.json"
            output_json(filepath, tested_dict)

            total_inspections = 0
            for d in inspections_list:
                total_inspections = total_inspections + int(d['検査検体数'])
            
            (dict_sub, list_sub) = conv_inspections_summary(records_dict)

            inspections_summary_dict = {
                "inspections_summary": {
                    "date" : inspections_date_str,
                    "data" : dict_sub,
                    "labels": list_sub
                }
            }
            
            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "inspections_summary.json"
            output_json(filepath, inspections_summary_dict)
            
        elif f_title == "patients_summary":
            
            df_fill = df.fillna({'患者判明数':0, '退院者数':0, '死亡者数':0, '軽症':0, '中等症':0, '重症':0})
            records_dict = df_fill.to_dict(orient='records')
            
            # patients_summary（患者判明数）
            patients_summary_list = conv_patients_summary_list(records_dict, 'patients')
            patients_summary_dict = {
                "patients_summary": {
                    "date" : now_date,
                    "data" : patients_summary_list
                }
            }
            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "patients_summary.json"
            output_json(filepath, patients_summary_dict)

            # discharges_summary（退院者数）
            discharge_summary_list = conv_patients_summary_list(records_dict, 'discharge')
            discharge_summary_dict = {
                "discharges_summary": {
                    "date" : now_date,
                    "data" : discharge_summary_list
                }
            }
            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "discharges_summary.json"
            output_json(filepath, discharge_summary_dict)

            # 患者判明数
            better_patients_summary_dict = conv_better_patients_summary_dict(records_dict, 'patients')

            total_patients = 0
            for k in better_patients_summary_dict:
                total_patients = total_patients + int(better_patients_summary_dict[k])
            
            # 退院者数
            better_discharge_summary_dict = conv_better_patients_summary_dict(records_dict, 'discharge')

            total_discharge = 0
            for k in better_discharge_summary_dict:
                total_discharge = total_discharge + int(better_discharge_summary_dict[k])
            
            # 死亡
            better_died_summary_dict = conv_better_patients_summary_dict(records_dict, 'died')
            
            total_died = 0
            for k in better_died_summary_dict:
                total_died = total_died + int(better_died_summary_dict[k])
            
            # 軽症
            better_mild_summary_dict = conv_better_patients_summary_dict(records_dict, 'mild')

            total_mild = 0
            for k in better_mild_summary_dict:
                total_mild = total_mild + int(better_mild_summary_dict[k])
            
            # 中等症
            better_medium_summary_dict = conv_better_patients_summary_dict(records_dict, 'medium')
            
            total_medium = 0
            for k in better_medium_summary_dict:
                total_medium = total_medium + int(better_medium_summary_dict[k])
            
            # 重症
            better_heavy_summary_dict = conv_better_patients_summary_dict(records_dict, 'heavy')

            total_heavy = 0
            for k in better_heavy_summary_dict:
                total_heavy = total_heavy + int(better_heavy_summary_dict[k])
            
            # better_patients_summary
            all_better_patients_summary_dict = {
                "better_patients_summary": {
                    "date" : now_date,
                    "data" : {
                        "感染者数": better_patients_summary_dict,
                        "退院者数": better_discharge_summary_dict,
                        "死亡者数": better_died_summary_dict,
                        "軽症": better_mild_summary_dict,
                        "中等症": better_medium_summary_dict,
                        "重症": better_heavy_summary_dict
                    }
                }
            }
            filepath = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR + "/" + "better_patients_summary.json"
            output_json(filepath, all_better_patients_summary_dict)
            
        else:
            print("wrong title")
            exit()

    gen_main_summary(total_visit,
                     total_patients,
                     total_discharge,
                     total_inspections,
                     total_died,
                     total_mild,
                     total_medium,
                     total_heavy)
        
    return()

def main():

    main_sub()
    
    return()

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
    BASE_URL = config.get(config_section, 'CKAN_URL')
    
    DEBUG = 0

    """
    hotline: 新型コロナコールセンター相談件数
    visit: 新型コロナ受診相談件数
    inspections: 検査実施数
    patients: 福岡市新型コロナ陽性患者発表情報
    """

    resource_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + RESOURCE_FILE
    DATA_DICT = load_json_file(resource_file_path)

    package_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + INPUT_DIR + "/" + "package.json"
    PACKAGE_DICT = load_json_file(package_file_path)
    
    main()
