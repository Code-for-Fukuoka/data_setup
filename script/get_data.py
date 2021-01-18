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
        use = DATA_DICT['resource'][f_title]['use']
        dataset = DATA_DICT['resource'][f_title]['dataset']

        api_com = 'package_show' + '?id=' + dataset
        url = BASE_URL + '/api/3/action/' + api_com

        if type == 'url' and use == 'True':
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
    elif encoding == 'utf-8':
        # print("P3", encoding)
        res = urllib.request.urlopen(url)
        res = res.read().decode('utf-8')
    else:
        # print("P4", encoding)
        res = urllib.request.urlopen(url)
        res = res.read()
    
    df = pd.read_csv(io.StringIO(res))
    
    return (df)

def gen_dummy_hotline():
    
    df = pd.DataFrame([[1, ORG_ID, "県名", "自治体名", "2020/01/01", "月", 0,""]], columns=['No','全国地方公共団体コード','都道府県名','市区町村名','年月日','曜日','件数','備考'])
    
    return(df)

# 以下を期間として、patients_summaryの初期（値が0の）データフレームを生成
# 　- 開始日：CKANから取得した検査実施数の開始日
# 　- 終了日：data_setupを実行した日
def gen_patients_df():

    yobi = ["月","火","水","木","金","土","日"]
    
    patients_filename = DATA_DICT['resource']['patients']['filename']

    df_patients_summary = pd.DataFrame(index=[],
                                       columns=['No','全国地方公共団体コード','都道府県名','市区町村名','年月日','曜日','件数','備考','患者判明数','退院者数','死亡者数','軽症','中等症','重症'])

    # CKANから取得した検査陽性者の状況のファイルを読み込み

    use_patients_status = DATA_DICT['resource']['patients_status']['use']

    if use_patients_status == 'True':
    
        patients_status_filename = DATA_DICT['resource']['patients_status']['filename']
        org_patients_status_filename = ORG_ID + "_" + patients_status_filename
        patients_status_filepath = I_FILEPATH + "/" + org_patients_status_filename
        df_patients_status = pd.read_csv(patients_status_filepath)

        for index, row in df_patients_status.iterrows():
            patients_status_date = row['公表_年月日']
        
        patients_status_pdate= datetime.datetime.strptime( patients_status_date, '%Y/%m/%d')
    
    # CKANから取得した検査実施数のファイルを取得
    inspections_filename = DATA_DICT['resource']['inspections']['filename']
    org_inspections_filename = ORG_ID + "_" + inspections_filename
    inspections_filepath = I_FILEPATH + "/" + org_inspections_filename
    df_inspections = pd.read_csv(inspections_filepath)

    inspections_org_id = df_inspections['全国地方公共団体コード'][0]
    inspections_pref_name = df_inspections['都道府県名'][0]
    inspections_town_name = df_inspections['市区町村名'][0]
    inspections_start_date = df_inspections['年月日'][0]
    inspections_start_pdate = datetime.datetime.strptime(inspections_start_date, '%Y/%m/%d')

    inspections_last_date = df_inspections['年月日'][len(df_inspections)-1]
    inspections_last_pdate = datetime.datetime.strptime(inspections_last_date, '%Y/%m/%d')
    
    # CKANから取得した陽性患者発表情報のファイルを読込み
    patients_filename = DATA_DICT['resource']['patients']['filename']
    org_patients_filename = ORG_ID + "_" + patients_filename    
    patients_filepath = I_FILEPATH + "/" + org_patients_filename
    df_patients = pd.read_csv(patients_filepath)

    """
    patients_org_id = df_patients['全国地方公共団体コード'][0]
    patients_pref_name = df_patients['都道府県名'][0]
    patients_town_name = df_patients['市区町村名'][0]
    patients_start_date = df_patients['公表_年月日'][0]
    patients_start_pdate = datetime.datetime.strptime(patients_start_date, '%Y/%m/%d')
    """

    patients_last_date = df_patients['公表_年月日'][len(df_patients)-1]
    patients_last_pdate = datetime.datetime.strptime(patients_last_date, '%Y/%m/%d')
    
    # find current date and month
    now = datetime.datetime.now()
    now_date = now.strftime('%Y/%m/%d')
    now_pdate = datetime.datetime.strptime(now_date, '%Y/%m/%d')

    if use_patients_status == 'True':
        end_pdate = patients_status_pdate
    else:
        end_pdate = patients_last_pdate
    
    count_pdate =  inspections_start_pdate

    new_sr_list = []
    
    line_count = 0
    while  end_pdate > count_pdate:

        line_count = line_count + 1

        count_pdate = count_pdate + datetime.timedelta(days=1)
        count_date = count_pdate.strftime('%Y/%m/%d')

        this_yobi = yobi[count_pdate.weekday()]

        new_sr = pd.Series({
            'No': line_count,
            '全国地方公共団体コード': inspections_org_id,
            '都道府県名': inspections_pref_name,
            '市区町村名': inspections_town_name,
            '年月日': count_date,
            '曜日': this_yobi,
            '件数': '',
            '備考': '',
            '患者判明数': 0,
            '退院者数': 0,
            '死亡者数': 0,
            '軽症': 0,
            '中等症': 0,
            '重症': 0
        })

        df_patients_summary = df_patients_summary.append(new_sr, ignore_index=True)

    return(df_patients_summary)
    
    
def gen_patients_summary(df_patients_summary):

    # CKANから取得した陽性患者発表情報のファイルを読込み
    patients_filename = DATA_DICT['resource']['patients']['filename']
    org_patients_filename = ORG_ID + "_" + patients_filename    
    patients_filepath = I_FILEPATH + "/" + org_patients_filename
    df_patients = pd.read_csv(patients_filepath)

    df_patients = df_patients.dropna(subset=['全国地方公共団体コード'])
    
    np_patients_date = df_patients.公表_年月日.values
    
    # 陽性患者発表情報を１件ずつチェック
    ## for index, row in df_patients.iterrows():
    for index in range(df_patients.shape[0]):

        ## patients_date = row['公表_年月日']
        patients_date = np_patients_date[index]
        
        patients_pdate = datetime.datetime.strptime( patients_date, '%Y/%m/%d')
        
        # 陽性患者者数の期間の日付に対し、陽性患者者発表情報の公表年月日を比較
        # 一致する場合、陽性患者者数を１加算

        np_summary_date = df_patients_summary.年月日.values
        
        ## for index2, row2 in df_patients_summary.iterrows():
        for index2 in range(df_patients_summary.shape[0]):
            
            ## summary_date = row2['年月日']
            summary_date = np_summary_date[index2]
            
            summary_pdate = datetime.datetime.strptime(summary_date, '%Y/%m/%d')

            if summary_pdate == patients_pdate:
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
        use = DATA_DICT['resource'][f_title]['use']
        dataset = DATA_DICT['resource'][f_title]['dataset']
        filename = DATA_DICT['resource'][f_title]['filename']

        if format == 'url':
            if use == 'True':
                url = resource_dict[f_title]['resources'][0]['url']
                # リソースのcsvファイルを取得し、文字コードをutf8へ変換後
                # dfに格納
                df = get_resource(f_title, url)
                # dfをcsvファイルに保存
                save_df(f_title, filename, df)
                
        elif format == "file":
            if use == 'True':
                if f_title == "patients_summary":

                    # 1. 以下を期間として、patients_summaryのデータを生成
                    # 　- 開始日：CKANから取得した検査実施数の開始日
                    # 　- 終了日：data_setupを実行した日
                    # 2. 陽性患者発表情報をから、patients_summaryの患者者数
                    #   をカウント
                    df_patients_summary_init = gen_patients_df()
                    df = gen_patients_summary(df_patients_summary_init)
                    save_df(f_title, filename, df)
                
                if f_title == "hotline":
                    # hotlineのダミーデータを生成
                    df = gen_dummy_hotline()
                    save_df(f_title, filename, df)
        else:
            print("wrong format:", "title=", f_title, "format=", format, "use=", use)
            exit()
            
    return()

def show_package_info(resource_dict):

    for f_title in DATA_DICT['resource']:
        format = DATA_DICT['resource'][f_title]['type']
        use = DATA_DICT['resource'][f_title]['use']

        if format == 'url' and use == 'True':
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

    WORK_DIR = os.path.dirname(os.path.abspath(__file__))
    WORK_DIR = os.path.dirname(WORK_DIR)
    TOOL_DIR = os.path.basename(WORK_DIR)
    WORK_DIR = os.path.dirname(WORK_DIR)
    
    INPUT_DIR = config.get(config_section, 'INPUT_DIR')
    OUTPUT_DIR = config.get(config_section, 'OUTPUT_DIR')
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
