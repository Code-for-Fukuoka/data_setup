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

""" defs
"""
def get_resource_file_dict(resource_file_dict_file):
    
    with open(resource_file_dict_file) as f:
        resource_file_dict = json.load(f)
        f.close()

    return(resource_file_dict)

def output_json(filepath, filename, o_dict):

    org_filename = ORG_ID + "_" + filename
    f_filepath = filepath + "/" + org_filename
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


def get_package_data():

    ckan_dict = {}
    resource_dict = {}
    
    for f_title in DATA_DICT['resource']:
        type = DATA_DICT['resource'][f_title]['type']
        dataset = DATA_DICT['resource'][f_title]['dataset']

        api_com = 'package_show' + '?id=' + dataset
        url = BASE_URL + '/api/3/action/' + api_com

        if type == "url":
            resp_dict = call_api(url)
            ckan_dict[f_title] = resp_dict
            resource_dict[f_title] = resp_dict['result']

    return(resource_dict)

def get_resource(f_title, url):

    res = urllib.request.urlopen(url)

    encoding = chardet.detect(res.read())['encoding']

    if encoding == None:
        # print("P0", encoding)
        res = urllib.request.urlopen(url)
        res = res.read().decode('shift-jis')
    elif encoding == 'SHIFT_JIS':
        # print("P1", encoding)
        res = urllib.request.urlopen(url)
        res = res.read().decode('shift-jis')
    elif encoding == 'UTF-8-SIG':
        # print("P2", encoding)
        res = urllib.request.urlopen(url)
        res = res.read().decode('utf-8-sig')
    else:
        # print("P3", encoding)
        res = urllib.request.urlopen(url)
        res = res.read()
    
    df = pd.read_csv(io.StringIO(res))
    
    return (df)

def gen_dummy_hotline():
    
    df = pd.DataFrame([[1, ORG_ID, "県名", "自治体名", "2020/01/01", "月", 0,""]], columns=['No','全国地方公共団体コード','都道府県名','市区町村名','年月日','曜日','件数','備考'])
    
    return(df)

def gen_patients_summary():

    inspections_filename = DATA_DICT['resource']['inspections']['filename']
    patients_filename = DATA_DICT['resource']['patients']['filename']
    
    # load inspections.csv
    org_inspections_filename = ORG_ID + "_" + inspections_filename
    inspections_filepath = I_FILEPATH + "/" + org_inspections_filename
    df_inspections = pd.read_csv(inspections_filepath)
    df_patients_summary = df_inspections
    
    # add column in inspections
    df_patients_summary['患者判明数'] = 0
    df_patients_summary['退院者数'] = 0
    df_patients_summary['死亡者数'] = 0
    df_patients_summary['軽症'] = 0
    df_patients_summary['中等症'] = 0
    df_patients_summary['重症'] = 0

    # load inspections.csv
    org_patients_filename = ORG_ID + "_" + patients_filename    
    patients_filepath = I_FILEPATH + "/" + org_patients_filename
    df_patients = pd.read_csv(patients_filepath)

    # check for each patients info
    for index, row in df_patients.iterrows():
        patients_date = row['公表_年月日']

        # find patients in each inspection's day
        for index2, row2 in df_patients_summary.iterrows():
            summary_date = row2['年月日']

            if summary_date == patients_date:
                patients_num = df_patients_summary.loc[index2, '患者判明数']
                df_patients_summary.loc[index2, '患者判明数'] = patients_num + 1
                break

    return(df_patients_summary)

def save_df(f_title, filename, df):

    org_filename = ORG_ID + "_" + filename
    filepath = I_FILEPATH + "/" + org_filename
    print("create:", org_filename)
    df.to_csv(filepath)

    return()

def get_resource_file(resource_dict):

    for f_title in DATA_DICT['resource']:
        format = DATA_DICT['resource'][f_title]['type']
        dataset = DATA_DICT['resource'][f_title]['dataset']
        filename = DATA_DICT['resource'][f_title]['filename']

        if format == 'url':
            url = resource_dict[f_title]['resources'][0]['url']
            # リソースのcsvファイルを取得し、文字コードをutf8へ変換後
            # dfに格納
            df = get_resource(f_title, url)
            # dfをcsvファイルに保存
            save_df(f_title, filename, df)
                
        elif format == "file":
            if f_title == "patients_summary":
                # patients_summaryのデータをinspectionとpatientsの
                # データから生成
                df = gen_patients_summary()
                save_df(f_title, filename, df)
                
            if f_title == "hotline":
                # hotlineのダミーデータを生成
                df = gen_dummy_hotline()
                save_df(f_title, filename, df)
        else:
            print("wrong format")
            exit()
            
    return()

def show_package_info(resource_dict):

    for f_title in DATA_DICT['resource']:
        format = DATA_DICT['resource'][f_title]['type']

        if format == "url":
            last_modified = resource_dict[f_title]["resources"][0]["last_modified"]
            print( f_title, last_modified)

    return()

def main():

    # パッケージのメタデータを取得
    resource_dict = get_package_data()

    show_package_info(resource_dict)
    
    filename = "package.json"
    output_json(I_FILEPATH, filename, resource_dict)
    
    get_resource_file(resource_dict)

if __name__ == '__main__':

    config = configparser.ConfigParser()
    path = os.getcwd()
    config.read('{}/../config.ini'.format(path), encoding="utf-8")
    config_section = 'development'

    WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')

    INPUT_DIR = config.get(config_section, 'INPUT_DIR')
    OUTPUT_DIR = config.get(config_section, 'OUTPUT_DIR')
    TOOL_DIR = config.get(config_section, 'TOOL_DIR')
    RESOURCE_FILE = config.get(config_section, 'RESOURCE_FILE')
    
    I_FILEPATH = WORK_DIR + "/" + TOOL_DIR + "/" + INPUT_DIR
    O_FILEPATH = WORK_DIR + "/" + TOOL_DIR + "/" + OUTPUT_DIR
    
    DEBUG = 1

    """
    hotline: 新型コロナコールセンター相談件数
    visit: 新型コロナ受診相談件数
    inspections: 検査実施数
    patients: 福岡市新型コロナ陽性患者発表情報
    """

    resource_file_path = WORK_DIR + "/" + TOOL_DIR + "/" + RESOURCE_FILE
    DATA_DICT = get_resource_file_dict(resource_file_path)

    ORG_ID = DATA_DICT['organization']['id']
    BASE_URL = DATA_DICT['organization']['url']

    main()
