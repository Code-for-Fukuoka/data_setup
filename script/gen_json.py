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
import math
import re

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

def find_area(residence):

    area = ''
    
    if re.match('調査中', residence):
        area = '調査中'
    elif re.match('確認中', residence):
        area = '調査中'
    elif re.match('海外', residence):
        area = '海外'
    elif re.match('福岡市', residence):
        
        residence_int = residence.replace('福岡市', '')

        if re.match('博多区', residence_int):
            area = '福岡市博多区'
        elif re.match('西区', residence_int):
            area = '福岡市西区'
        elif re.match('東区', residence_int):
            area = '福岡市東区'
        elif re.match('中央区', residence_int):
            area = '福岡市中央区'
        elif re.match('早良区', residence_int):
            area = '福岡市早良区'
        elif re.match('城南区', residence_int):
            area = '福岡市城南区'
        elif re.match('南区', residence_int):
            area = '福岡市南区'
        else:
            area = '福岡市内'
            
    elif re.match('北九州市', residence):

        residence_int = residence.replace('北九州市', '')
        
        if re.match('門司区', residence_int):
            area = '北九州市門司区'
        elif re.match('若松区', residence_int):
            area = '北九州市若松区'
        elif re.match('戸畑区', residence_int):
            area = '北九州市戸畑区'
        elif re.match('小倉北区', residence_int):
            area = '北九州市小倉北区'
        elif re.match('小倉南区', residence_int):
            area = '北九州市小倉南区'
        elif re.match('八幡東区', residence_int):
            area = '北九州市八幡東区'
        elif re.match('八幡西区', residence_int):
            area = '北九州市八幡西区'
        else:
            area = '北九州市内'
        
    elif re.match('久留米市', residence):
        area = '久留米市'
    elif re.match('福岡県', residence):
        area = '福岡県'
    elif residence in CITY_LIST:
        for city in CITY_LIST:
            if residence == city:
                area = city
                break
    else:
        area = '県外：'+residence
    
    return(area)

def conv_patients(records_dict, infection_route_info):
    
    records_list = []

    record_count = 0
    for record in records_dict:

        record_count += 1
        
        date = record['公表_年月日']
        dayofweek = record['曜日']

        if type(record['居住地']) is float:
            if math.isnan(record['居住地']):
                residence = '調査中'
        else:
            residence = record['居住地']

        area = find_area(residence)

        age = record['年代']
        ageOrg = age

        # collect invalid age input
        if re.match(r'1[a-zA-Z0-9]代未満', age):
            age = '10代未満'
        elif re.match(r'1[a-zA-Z0-9]歳未満', age):
            age = '10代未満'
        elif re.match(r'1[a-zA-Z0-9]代', age):
            age = '10代'
        elif re.match(r'2[a-zA-Z0-9]代', age):
            age = '20代'
        elif re.match(r'3[a-zA-Z0-9]代', age):
            age = '30代'
        elif re.match(r'4[a-zA-Z0-9]代', age):
            age = '40代'
        elif re.match(r'5[a-zA-Z0-9]代', age):
            age = '50代'
        elif re.match(r'6[a-zA-Z0-9]代', age):
            age = '60代'
        elif re.match(r'7[a-zA-Z0-9]代', age):
            age = '70代'
        elif re.match(r'8[a-zA-Z0-9]代', age):
            age = '80代'
        elif re.match(r'9[a-zA-Z0-9]代', age):
            age = '90代'
        elif re.match(r'9[a-zA-Z0-9]歳以上', age):
            age = '90代'            
        elif re.search(r'-|‐', age):
            age = '調査中'
        
        sex = record['性別']
        if re.search(r'-|‐', sex):
            sex = '調査中'
        elif sex == '女':
            sex = '女性'
        elif sex == '男':
            sex = '男性'
            
        
        """
        if record['退院済フラグ'] == 1:
            discharge = '○'
        else: 
            discharge = ''
        """
            
        discharge = ''

        if infection_route_info:
            if record['感染経路不明'] == 1:
                infection_route = '感染経路不明'
            elif record['濃厚接触者'] == 1:
                infection_route = '濃厚接触者'
            elif record['海外渡航歴有'] == 1:
                infection_route = '海外渡航歴有'
            else:
                infection_route = ''
        else:
                infection_route = ''

        # make Number of Week
        numofweek = get_numofweek(dayofweek)
        # make date and time
        (date, time) = get_datetime(date)
        dateandtime = date + 'T' + time + 'Z'

        record_dict= {}
        record_dict["リリース日"] = dateandtime
        record_dict["曜日"] = 0
        # record_dict["居住地"] = residence
        record_dict["居住地"] = area
        # record_dict["地域"] = area
        record_dict["年代"] = age
        record_dict["性別"] = sex
        record_dict["退院"] = discharge
        
        if infection_route_info:
            record_dict["感染経路"] = infection_route
            
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
                     total_inspections,
                     patients_status):

    data_title = "main_summary"

    total_patients = patients_status['total_patients']
    total_hospitalized = patients_status['total_hospitalized']
    total_died = patients_status['total_died']
    total_discharge = patients_status['total_discharge']
    total_mild = patients_status['total_mild']
    total_medium = patients_status['total_medium']
    total_heavy = patients_status['total_heavy']

    type = DATA_DICT['resource']['patients_status']['type']
    use = DATA_DICT['resource']['patients_status']['use']
    # date in main_summary
    # if patients_status is available use its date, otherwise use patietsns's date
    if type == 'url' and use == 'True':
        patients_status_date = PACKAGE_DICT["patients_status"]["resources"][0]["last_modified"]
    else:
        patients_status_date = PACKAGE_DICT["patients"]["resources"][0]["last_modified"]
    patients_status_date_str = conv_time(patients_status_date)
                     
    main_summary_dict = {
        data_title: {
            "attr": "検査実施人数",
            "value": total_inspections,
            "date": patients_status_date_str,
            "children": [
                {
                    "attr": "陽性患者数",
                    "value": total_patients,
                    "children": [
                        {
                            "attr": "入院中",
                            "value": total_hospitalized,
                            "children": [
                                {
                                    "attr": "軽症・中等症",
                                    # "value": total_mild + total_medium
                                    "value": '-'
                                },
                                {
                                    "attr": "重症",
                                    # "value": total_heavy
                                    "value": '-'
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

    filename = data_title + ".json"
    output_json(O_FILEPATH, filename, main_summary_dict)
    
    return()

def get_date_label(date):

    date_list = date.split('/')

    month = date_list[1]
    day = date_list[2]

    # date_label = day + '\/' + month
    # date_label = day + '/' + month
    date_label = month + '/' + day
    
    return(date_label)

def conv_inspections_summary(records_dict):

    city_list = []
    fukuoka_city_list = []
    kitakyushu_city_list = []
    others_list = []
    private_list = []
    label_list = []

    if ORG_ID == "400009":

        for record in records_dict:

            num = int(float(record['件数']))
            num_fukuoka_city = int(float(record['福岡市']))
            num_kitakyushu_city = int(float(record['北九州市']))
            num_others = int(float(record['福岡県']))

            if '民間検査' in record:
                num_private = int(float(record['民間検査']))
            else:
                num_private = 0
        
            date = record['年月日']
            date_label = get_date_label(date)

            city_list.append(num)
            fukuoka_city_list.append(num_fukuoka_city)
            kitakyushu_city_list.append(num_kitakyushu_city)
            others_list.append(num_others)
            private_list.append(num_private)
            label_list.append(date_label)
            
        inspections_summary_dict = {
            "福岡市": fukuoka_city_list,
            "北九州市": kitakyushu_city_list,
            "福岡県※": others_list,
            "民間検査": private_list
        }
        
    else:

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

def output_json(o_filepath, filename, o_dict):

    org_filename = ORG_ID + "_" + filename
    f_filepath = o_filepath + "/" + org_filename

    f = open(f_filepath, 'w')
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

def gen_total_discharge():

    org_filename = ORG_ID + "_" + "patients.json"
    file_path = O_FILEPATH + "/" + org_filename

    patients_dict = load_json_file(file_path)

    total_discharge = 0
    for d in patients_dict['patients']['data']:
        if d['退院'] == '○':
            total_discharge = total_discharge + 1
        
    return(total_discharge)

def gen_total_patients():

    org_filename = ORG_ID + "_" + "patients.json"
    file_path = O_FILEPATH + "/" + org_filename

    patients_dict = load_json_file(file_path)

    total_patients = 0
    for d in patients_dict['patients']['data']:
        total_patients = total_patients + 1
        
    return(total_patients)

def load_input_file(filename):

    org_filename = ORG_ID + "_" + filename
    file_path = I_FILEPATH + "/" + org_filename

    print("load:", org_filename)
        
    df = pd.read_csv(file_path, index_col=0)
    
    return(df)

def gen_hotline():

    f_title = "hotline"
    
    filename = DATA_DICT['resource'][f_title]['filename']
    type = DATA_DICT['resource'][f_title]['type']
    
    data_title = "contacts"
            
    df = load_input_file(filename)
    df_fill = df.fillna({'件数':0})
    records_dict = df_fill.to_dict(orient='records')
    hotline_list = conv_hotline(records_dict)

    if type == 'url':
        hotline_date = PACKAGE_DICT["hotline"]["resources"][0]["last_modified"]
    else:
        hotline_date = "2020-01-01T00:00:00.000000"
                
    hotline_date_str = conv_time(hotline_date)
            
    hotline_dict = {
        data_title : {
            "date" : hotline_date_str,
            "data" : hotline_list
        }
    }

    filename = data_title + ".json"
    output_json(O_FILEPATH, filename, hotline_dict)

    return()

def gen_visit():

    f_title = "visit"
    
    filename = DATA_DICT['resource'][f_title]['filename']
    type = DATA_DICT['resource'][f_title]['type']
    
    data_title = "querents"
            
    df = load_input_file(filename)
    df_fill = df.fillna({'件数':0})
    records_dict = df_fill.to_dict(orient='records')
    visit_list = conv_visit(records_dict)

    if type == 'url':
        visit_date = PACKAGE_DICT["visit"]["resources"][0]["last_modified"]
    else:
        visit_date = "2020-01-01T00:00:00.000000"
            
    visit_date_str = conv_time(visit_date)
            
    visit_dict = {
        data_title : {                
            "date" : visit_date_str,
            "data" : visit_list
        }
    }
            
    total_visit = 0
    for d in visit_list:
        total_visit = total_visit + int(d['小計'])
            
    filename = data_title + ".json"
    output_json(O_FILEPATH, filename, visit_dict)

    return(total_visit)

def gen_patients():

    f_title = "patients"
    
    filename = DATA_DICT['resource'][f_title]['filename']
    type = DATA_DICT['resource'][f_title]['type']
    
    data_title = f_title

    df = load_input_file(filename)

    # 空白行の削除に対応
    # 　全国地方公共団体コードが空白の場合に削除
    df = df.dropna(subset=['全国地方公共団体コード'])
    df = df.dropna(subset=['公表_年月日'])
    
    # df_fill = df.fillna({'退院済フラグ':0})
    df_fill = df
    
    records_dict = df_fill.to_dict(orient='records')

    if '感染経路不明' in df_fill and '濃厚接触者' in df_fill and '海外渡航歴有' in df_fill:
        infection_route_info = True
    else:
        infection_route_info = False
    
    patients_list = conv_patients(records_dict, infection_route_info)

    if type == 'url':
        patients_date = PACKAGE_DICT["patients"]["resources"][0]["last_modified"]
    else:
        patients_date = "2020-01-01T00:00:00.000000"
    patients_date_str = conv_time(patients_date)
            
    patients_dict = {
        data_title : {                
            "date" : patients_date_str,
            "data" : patients_list
        }
    }
            
    filename = data_title + ".json"
    output_json(O_FILEPATH, filename, patients_dict)

    return()

def gen_inspections():

    f_title = "inspections"
    
    filename = DATA_DICT['resource'][f_title]['filename']
    type = DATA_DICT['resource'][f_title]['type']
    
    data_title  = f_title
    data_title2 = "tested"
    data_title3 = "inspections_summary"
            
    df = load_input_file(filename)

    if ORG_ID == '400009':
        df_fill = df.fillna({'件数':0, '福岡県':0, '福岡市':0, '北九州市':0})
    else:
        df_fill = df.fillna({'件数':0})
    
    records_dict = df_fill.to_dict(orient='records')
    inspections_list = conv_inspections(records_dict)
    tested_list = conv_tested(records_dict)

    if type == 'url':
        inspections_date = PACKAGE_DICT["inspections"]["resources"][0]["last_modified"]
    else:
        inspections_date = "2020-01-01T00:00:00.000000"
    inspections_date_str = conv_time(inspections_date)
            
    inspections_dict = {
        data_title : {                
            "date" : inspections_date_str,
            "data" : inspections_list
        }
    }

    tested_dict =  {
        data_title2: {
            "date" : inspections_date_str,
            "data" : tested_list
        }
    }
            
    filename = data_title + ".json"
    output_json(O_FILEPATH, filename, inspections_dict)

    filename = data_title2 + ".json"
    output_json(O_FILEPATH, filename, tested_dict)

            
    total_inspections = 0
    for d in inspections_list:
        total_inspections = total_inspections + int(d['検査検体数'])
            
    (dict_sub, list_sub) = conv_inspections_summary(records_dict)

    inspections_summary_dict = {
        data_title3: {
            "date" : inspections_date_str,
            "data" : dict_sub,
            "labels": list_sub
        }
    }
            
    filename = data_title3 + ".json"
    output_json(O_FILEPATH, filename, inspections_summary_dict)

    return(total_inspections)

def gen_patients_summary(now_date):

    f_title = "patients_summary"
    
    filename = DATA_DICT['resource'][f_title]['filename']
    type = DATA_DICT['resource'][f_title]['type']
    
    data_title  = f_title
    data_title2 = "discharges_summary"
    data_title3 = "better_patients_summary"
            
    df = load_input_file(filename)
    df_fill = df.fillna({'患者判明数':0,
                         '退院者数':0,
                         '死亡者数':0,
                         '軽症':0,
                         '中等症':0,
                         '重症':0})
            
    records_dict = df_fill.to_dict(orient='records')
    
    # patients_summary（患者判明数）
    patients_summary_list = conv_patients_summary_list(records_dict, 'patients')
    patients_summary_dict = {
        data_title : {
            "date" : now_date,
            "data" : patients_summary_list
        }
    }

    filename = data_title + ".json"
    output_json(O_FILEPATH, filename, patients_summary_dict)
            
    # discharges_summary（退院者数）
    discharge_summary_list = conv_patients_summary_list(records_dict, 'discharge')
    discharge_summary_dict = {
        data_title2: {
            "date" : now_date,
            "data" : discharge_summary_list
        }
    }
            
    filename = data_title2 + ".json"
    output_json(O_FILEPATH, filename, discharge_summary_dict)
            
    # 患者判明数
    better_patients_summary_dict = conv_better_patients_summary_dict(records_dict, 'patients')

    total_patients = gen_total_patients()
                
    # 退院者数
    better_discharge_summary_dict = conv_better_patients_summary_dict(records_dict, 'discharge')

    total_discharge = gen_total_discharge()

    # 死亡者数(dummy data)
    better_died_summary_dict = conv_better_patients_summary_dict(records_dict, 'died')

    total_died = '-'
                
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
        data_title3: {
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
            
    filename = data_title3 + ".json"
    output_json(O_FILEPATH, filename, all_better_patients_summary_dict)

    patients_status={}
    
    patients_status['total_patients'] = total_patients
    patients_status['total_discharge'] = total_discharge
    patients_status['total_hospitalized'] = total_patients - total_discharge
    patients_status['total_mild'] = total_mild
    patients_status['total_medium'] = total_medium
    patients_status['total_heavy'] = total_heavy
    patients_status['total_died'] = total_died
        
    return(patients_status)


def gen_patients_status_daily_dict(df_patients):

    patients_list_cont = []

    for index, row in df_patients.iterrows():

        data = {}

        data['公表_年月日'] = row['公表_年月日']
        data['曜日'] = row['曜日']
        
        if math.isnan(row['陽性者数累計']):
            data['陽性者数累計'] = row['陽性者数累計']
        else:
            data['陽性者数累計'] = int(row['陽性者数累計'])
            
        if math.isnan(row['退院者数累計']):
            data['退院者数累計'] = row['退院者数累計']
        else:
            data['退院者数累計'] = int(row['退院者数累計'])
            
        if math.isnan(row['死亡者数累計']):
            data['死亡者数累計'] = row['死亡者数累計']
        else:
            data['死亡者数累計'] = int(row['死亡者数累計'])

        if math.isnan(row['入院・療養者数']):
            data['入院・療養者数'] = '確認中'
        else:
            data['入院・療養者数'] = int(row['入院・療養者数'])
            
        if math.isnan(row['入院中の者の数']):
            data['入院中の者の数'] = 'NA'
        else:
            data['入院中の者の数'] = int(row['入院中の者の数'])
            
        if math.isnan(row['うち確保病床の入院者数']):
            data['うち確保病床の入院者数'] = 'NA'
        else:
            data['うち確保病床の入院者数'] = int(row['うち確保病床の入院者数'])
            
        if math.isnan(row['宿泊療養中の者の数']):
            data['宿泊療養中の者の数'] = 'NA'
        else:
            data['宿泊療養中の者の数'] = int(row['宿泊療養中の者の数'])
            
        if math.isnan(row['自宅待機等の者の数']):
            data['自宅待機等の者の数'] = 'NA'
        else:
            data['自宅待機等の者の数'] = int(row['自宅待機等の者の数'])

        patients_list_cont.append(data)
        
    return(patients_list_cont)

def gen_patients_status_daily(now_date):

    f_title = "patients_status"
    filename = DATA_DICT['resource'][f_title]['filename']
    
    type = DATA_DICT['resource'][f_title]['type']
    
    df = load_input_file(filename)
    df_fill = df.fillna({'件数':0})
    df_patients = df_fill

    patients_status_type = check_patients_status_type(df_patients)
    
    if patients_status_type == 'new':
        filename = f_title + '_daily' + '.csv'
        df_patients = load_input_file(filename)
        patients_list_cont = gen_patients_status_daily_dict(df_patients)
    else:
        patients_list_cont = []


    data_title = 'patients_status_daily'
    
    patients_dict = {
        data_title : {
        'date': now_date,
        'data': patients_list_cont
            }
    }
        
        
    filename = DATA_DICT['resource'][f_title]['filename']
    filename = f_title + '_daily' + '.json'
    
    output_json(O_FILEPATH, filename, patients_dict)
        
    return(patients_dict)

def check_patients_status_type(df_patients):

    new_column = [ '全国地方公共団体コード',
                   '都道府県名',
                   '市区町村名',
                   '公表_年月日',
                   '曜日',
                   # '陽性者数累計',
                   '退院者数累計',
                   '死亡者数累計',
                   '入院・療養者数',
                   '入院中の者の数',
                   'うち確保病床の入院者数',
                   '宿泊療養中の者の数',
                   '自宅待機等の者の数' ]

    new_column_type = True
    
    for item in new_column:
        if item not in df_patients.columns.values:
            new_column_type = False

    if new_column_type == True:
        patients_status_type = 'new'
    else:
        patients_status_type = 'old'
        
    return(patients_status_type)

def gen_patients_status():

    f_title = "patients_status"
    
    filename = DATA_DICT['resource'][f_title]['filename']
    type = DATA_DICT['resource'][f_title]['type']
    
    df = load_input_file(filename)
    df_fill = df.fillna({'件数':0})
    df_patients = df_fill

    patients_status_type = check_patients_status_type(df_patients)
    
    latest_date_p = datetime.datetime.strptime('2020/03/01', "%Y/%m/%d")
    latest_index = 0
    latest_patients = 0
    latest_hospitalized = 0
    latest_died = 0
    latest_discharged = 0

    patients_status={}
    
    for index, row in df_patients.iterrows():

        date_str = row['公表_年月日']
        date_p = datetime.datetime.strptime(date_str, "%Y/%m/%d")
        
        if date_p > latest_date_p:
            
            latest_date_p = date_p
            latest_index = index
            latest_patients = row['陽性患者数累計']
            
            if patients_status_type == 'old':
                latest_hospitalized = row['入院者数累計']
            elif patients_status_type == 'new':
                if math.isnan(row['入院・療養者数']):
                    latest_hospitalized = '確認中'
                else:
                    latest_hospitalized = int(row['入院・療養者数'])
                
            latest_died = row['死亡者数累計']
            latest_discharged = row['退院者数累計']

        patients_status['total_patients'] = latest_patients
        patients_status['total_hospitalized'] = latest_hospitalized
        patients_status['total_died'] = latest_died
        patients_status['total_discharge'] = latest_discharged
                     
    patients_status['total_mild'] = '-'
    patients_status['total_medium'] = '-'
    patients_status['total_heavy'] = '-'

    return(patients_status)

def main_sub():

    now = datetime.datetime.now()
    now_date = now.strftime('%Y/%m/%d %H:%M')
    now_date = now_date.replace('/', r'\/')

    for f_title in DATA_DICT['resource']:

        # 新型コロナウイルス感染症　相談ダイヤル相談件数
        if f_title == "hotline":

            use = DATA_DICT['resource'][f_title]['use']
            if use == 'True':
                
                gen_hotline()

        # 新型コロナウイルス感染症　帰国者・接触者相談センター相談件数
        elif f_title == "visit":

            use = DATA_DICT['resource'][f_title]['use']
            if use == 'True':
                
                total_visit = gen_visit()

        # 陽性患者数
        elif f_title == "patients":

            use = DATA_DICT['resource'][f_title]['use']
            if use == 'True':
                
                gen_patients()

        # 検査実施数
        elif f_title == "inspections":

            use = DATA_DICT['resource'][f_title]['use']
            if use == 'True':
                
                total_inspections = gen_inspections()

        # 陽性患者の属性
        elif f_title == "patients_summary":

            use = DATA_DICT['resource'][f_title]['use']
            if use == 'True':
                
                patients_summary_status = gen_patients_summary(now_date)

        # 検査陽性者の状況(データが提供される場合)
        # データが提供されない場合は陽性患者の属性のデータを利用
        elif f_title == "patients_status":
            
            use = DATA_DICT['resource'][f_title]['use']
            if use == 'True':
                
                patients_status_status = gen_patients_status()

                patients_status_dict = gen_patients_status_daily(now_date)
                    
        else:

            use = DATA_DICT['resource'][f_title]['use']
            if use == 'True':
                
                print("wrong title")
                exit()

    # 検査陽性者の状況
    use_patients_summary = DATA_DICT['resource']['patients_summary']['use']
    use_patients_status = DATA_DICT['resource']['patients_status']['use']

    if use_patients_status == 'True':
        patients_status = patients_status_status
    else:
        patients_status = patients_summary_status
    
    gen_main_summary(total_visit,
                     total_inspections,
                     patients_status)
        
    return()

def load_city_list(city_list_file_path):
    
    df = pd.read_csv(city_list_file_path)

    city_list = []

    for index, row in df.iterrows():

        city_name = row['town']
        city_list.append(city_name)

    return(city_list)

def main():

    main_sub()
    
    return()

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
    
    DEBUG = 0

    """
    hotline: 新型コロナコールセンター相談件数
    visit: 新型コロナ受診相談件数
    inspections: 検査実施数
    patients: 福岡市新型コロナ陽性患者発表情報
    """

    resource_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + RESOURCE_FILE
    DATA_DICT = load_json_file(resource_file_path)

    ORG_ID = DATA_DICT['organization']['id']
    
    org_package_file = ORG_ID + "_" + "package.json"
    package_file_path = I_FILEPATH + "/" + org_package_file
    PACKAGE_DICT = load_json_file(package_file_path)

    city_list_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + "script/000618153.csv"
    CITY_LIST = load_city_list(city_list_file_path)

    main()
