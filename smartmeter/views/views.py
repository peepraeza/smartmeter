#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ..models import Meter
from ..post_data import parse_keys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from datetime import datetime, timedelta
import requests
import pytz
import numpy as np
import base64, zlib, time
import threading
import os, glob
import urllib3
from statistics import mean 
import pandas as pd

urllib3.disable_warnings()

time_data, p1, p2, p3, p4, q1, q2, q3, q4, s1, s2, s3, s4 , pf1 = ([] for i in range(14))
i1, i2, i3, i4, p1_wh, p2_wh, p3_wh, p4_wh = ([] for i in range(8))

tz = pytz.timezone('Asia/Bangkok')
list_nodes = ['X', 'A', 'B', 'C']

def unixtime_to_readable(unixtime):
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.fromtimestamp(unixtime, tz)
    month = now.month
    year = now.year
    day = now.day
    hour = now.strftime('%H')
    minute = now.strftime('%M')
    second = now.strftime('%S')
    return (str(year), str(month), str(day), hour, minute, second)

key = {
    "type": "service_account",
    "project_id": "data-log-fb39d",
    "private_key_id": "80fcc158210ed58b29588b3a67d52c170c60d0d4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDnosoCGh4cByPb\nmXVsjoBR+jOhgh58Z8qrU6Z33MhIQ045fHsscz1ncI7HsgNC5jQ7dQ6ZY0IB9sMq\n0Z3JUo3KMS9lpsd/MAs8oq+zmU39QsGTm+Ha7kiTQuI4PjkOfUB9oyVcdyP6TXUk\nrAzrIAwJfnar5NKmFcpK6EsNzsumx2QVQaC/zK8VAQou8KBmEDc6VsHhUWFh6j9p\nSN0iCw8hWXjVRI/r1ReUs9kR+30QDSXnNIO77a8XFmZyC2maEnqPY6vSeRP1cTWa\nHHackO8TxnhR4siLwZ7o4LVe25ocLIbzC6PnzCDXgG7Vk/Yc2UsGdogcjgbGvjP9\n6yq5iWEvAgMBAAECggEARLStdIgorCmWAjn3cXanKymqjNpajo3+uGi8dMshAQYt\nurFom5um9/qT7zmm6/36OjSTWv3tA0YdR6MbSS7abcG/DEi23cvzWU3sDbqIPnnB\njzXqfRS2pC9viD00kU6nhVyR5WZVXpYBDBqYTlmYGGzRaFUcAjVuZl+We4b+Mv5b\nA/eWRx9AoJEy0Vr4HexEeJI+mJCOag+Ab1Kk4YkOpTLgDhnHHLfzn5n+H4Da8VaS\n5//4uFCDF5TIwHz4L3qZCWudDlVq6UF4390IpQTMMdyDgQJfeiesvQdcPKzae9EV\nYBo/QftB/kbZ66RukVAgIVEOf3vJtZplcfm+8MJokQKBgQD08/cnT2pze5hk7NnL\n09aSTYs/v7YKTQVgy5dCmQ5s/9KtS0KNnH2wbM/gIvmDSdsSoLVsSylybgShxF/f\n8yqprmtdPxw8jIkHUnyZIKBQAKYTXTfZF5QUgJ3E8qGxJ3xBUWGr4ZvdiXkDW4B4\n9O1VGhBMvy9DIN9GliF8yilnqQKBgQDyFRMvnXtgYj6T0IhAj8wEVuQy4V1MpLEb\neV8bmyX03vYm9h4fdd/OntrSwx1IfDP+q76SX4L2y6dlBoO3vS2HJ/9EbDeK35/C\nscwiToaoVljVZwGOqjkeMr1fH9DvQVBX8pupgVQtG3lERzl0GUgJBsMUID9JbkSp\nDSPq0t8pFwKBgGTJ9YoxPSXjVyM/6aXatlFgoslKQsceRfY8DzMR80OaR7+SVgIa\nwATV4PriqTQCMagKhFvY2WcCKdm+CY0GaymCYR7vFtk7Ii7nG+mN6SjB+5PAKXik\nIQQGn+QnyawxCQl/SOcGX7HaHPbqsYQTk4wOu2I40GOYpQZQQ9sq+7pxAoGBAIWk\nhNcAhaAMHKfVs6KQv/yVS52bNLqfIPcd5heDa0zn2dRggvizRj73C67W8E+X4cxy\nW97Kw64jd+IZ2pWQ5pV6yz2m0HLmSXheV2eJGmXMZXZKS13LM4UsVccx9VJgKE6l\nLLJDJ4lPZX8AIwOpAU+aYA+4TbfoHBeHnZCBoZk5AoGBANjr5irUefz0Q9N1qUWi\nfX9phEKXRxPt9RQlx3TQuUh64kfoaIOlOZrT70GlFjPwgi2OSDzY7LFsSw1YNU3E\n++GeVXcxcjEAAUrxbfBS89sN8Qv3GSe/Kl3TH9MJ0cEfmbmH/UOw9ktqpPDJBHBF\n8PGSHAkwT18oMazDVlTJqlNc\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-qthge@data-log-fb39d.iam.gserviceaccount.com",
    "client_id": "111119234437985151574",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-qthge%40data-log-fb39d.iam.gserviceaccount.com"
}

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://data-log-fb39d.firebaseio.com/'
})

    
def index(request):
    last_4_hours = datetime.now() - timedelta(hours = 4)
    ref = db.reference('energy')
    start = datetime.now()
    result = ref.order_by_child('time').limit_to_last(1800).get() # 3 hr
    end = datetime.now()
    print(end - start)
    _m = Meter.objects.all()
    module_dir = os.path.dirname(__file__)
    bill_path = os.path.join(module_dir, '../../static/json/setting.json')
    data_bill = open(bill_path , 'r')  
    data = json.load(data_bill)
    dbill = data["bill-cycle"]
    return render(request, "index.html", {"energy": json.dumps(list(result.values())), 
                                          "dec_time1": 0,
                                          "dec_time2": 0,
                                          "dec_time3": 0,
                                          "dec_time4": 0,
                                          "meter": _m, "dbill": dbill })

def setting(request):
    global p1_wh
    module_dir = os.path.dirname(__file__)  
    ip_path = os.path.join(module_dir, '../../static/json/ip.txt')
    bill_path = os.path.join(module_dir, '../../static/json/setting.json')
    data_ip = open(ip_path , 'r')   
    data_bill = open(bill_path , 'r')  
    data = json.load(data_bill)
    dbill = data["bill-cycle"]
    dunit = data["unit"]
    ip = data_ip.read()
    _m = Meter.objects.all()
    _range = range(1,32)
    print(len(p1_wh))
    return render(request, "setting.html",{"meter": _m, "ip_now" : ip, 
                                           "range": _range, "dbill":dbill, "unit": dunit})

def history(request):
    return render(request,"history.html")
    
def del_history(request):
    return redirect("/history/")
    
def graph(request):
    return render(request, "graph.html")

def save_json(keep_day, d_1m, d_30m, d_1hr, p1_wh, p2_wh, p3_wh, p4_wh, list_column):
    print("open save json")
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, '../../static/json/data_energy/')
    time_data = unixtime_to_readable(keep_day[0])
    year = time_data[0]
    month = time_data[1]
    day = time_data[2]
    dic_data = {}
    time = ["1m", "30m", "1hr"]
    keep_json = {"sum_p1" : round(p1_wh,2), "sum_p2" : round(p2_wh,2), "sum_p3" : round(p3_wh,2), "sum_p4" : round(p4_wh,2)}
    for t in time:
        dic_data = {}
        data = {}
        for n in list_column:
            data[n] = list(eval("d_{}[n]".format(t)))
        dic_data[t] = data
        keep_json.update(dic_data)         
    file_name = day.zfill(2)+"-"+month.zfill(2)+"-"+year
    with open(file_path+file_name+".json", 'w+') as f:
        json.dump(keep_json, f, ensure_ascii=False)
    print("upload json "+file_name)

def keep_data_realtime(d, wh, time_data, keep_day, keep_hour, keep_minute, check30):
    ref = db.reference('energy')
    print("get old value prepare at "+str(int(time.time())))
    if(len(time_data)>0):
        get_start = time_data[len(time_data)-1]
    else:
        keep_date = unixtime_to_readable(time.time())
        new_date = keep_date[2]+'-'+keep_date[1]+'-'+keep_date[0]
        get_start = int(time.mktime(datetime.strptime(new_date, "%d-%m-%Y").timetuple())) - 25200
    result = ref.order_by_child('time').start_at(int(get_start)).end_at(int(time.time())).get()
    for val in result.values():
        time_value = val["time"]
        keep_day, keep_hour, keep_minute, check30, d, wh, time_data = check_condition(val, time_value,keep_day, keep_hour, keep_minute, check30, d, wh, time_data)

    print("real time start at "+str(int(time.time())))
    time_before = 0
    print(len(time_data))
    while(True):
        result = ref.order_by_child('time').limit_to_last(1).get()
        for val in result.values():
            time_value = val["time"]
            if(time_before != time_value):
                print(unixtime_to_readable(time_value))
                time_before = time_value
                keep_day, keep_hour, keep_minute, check30, d, wh, time_data = check_condition(val, time_value,keep_day, keep_hour, keep_minute, check30, d, wh, time_data)
                time.sleep(1)
                                
def backup_from_firebase():
    print("Start Backup")
    t_start = datetime.now()
    d_1m, d_30m, d_1hr, d_1m_cur, d_30m_cur, d_1hr_cur = (pd.DataFrame() for i in range(6))
    p1_wh_value, p2_wh_value, p3_wh_value, p4_wh_value = (0 for i in range(4))
    d = [d_1m, d_30m, d_1hr, d_1m_cur, d_30m_cur, d_1hr_cur]
    wh = [p1_wh_value, p2_wh_value, p3_wh_value, p4_wh_value]
    time_data = []

    ref = db.reference('energy')
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, '../../static/json/data_energy')
    list_of_files = glob.glob(file_path+'/*') # * means all if need specific format then *.csv
    print(list_of_files)
    if(len(list_of_files) > 0):
        latest_file = list_of_files[len(list_of_files)-1]
        _, s = os.path.split(latest_file)
        _d = int(os.path.splitext(s)[0].split('-')[0]) + 1
        _m = os.path.splitext(s)[0].split('-')[1]
        _y = os.path.splitext(s)[0].split('-')[2]
        new_date = str(_d).zfill(2)+'-'+_m.zfill(2)+'-'+_y
        print(new_date)
        start = int(time.mktime(datetime.strptime(new_date, "%d-%m-%Y").timetuple())) - 25200
    else:
        start = 1549386000

    endt = int(time.time())
    print("end", unixtime_to_readable(endt))
    print("start", unixtime_to_readable(start))
    result = ref.order_by_child('time').start_at(int(start)).end_at(int(endt)).get()  
    print("get firebase complete")
    check30 = True	
    for val in result.values():
        time_value = val["time"]
        keep_date = unixtime_to_readable(time_value) 
        keep_day = keep_date[2]
        keep_hour = keep_date[3]
        keep_minute = keep_date[4]  
        break
    for val in result.values():
        time_value = val["time"]
        keep_day, keep_hour, keep_minute, check30, d, wh, time_data = check_condition(val, time_value,keep_day, keep_hour, keep_minute, check30, d, wh, time_data)

    print("-----------------------------Complete--------------------------------------")
    print(datetime.now()-t_start)
    print(time_data)
    print(len(time_data))
    keep_data_realtime(d, wh, time_data, keep_day, keep_hour, keep_minute, check30)

def check_condition(val, time_value, keep_day, keep_hour, keep_minute, check30, d, wh, time_data):
    d_1m, d_30m, d_1hr, d_1m_cur, d_30m_cur, d_1hr_cur = d
    p1_wh_value, p2_wh_value, p3_wh_value, p4_wh_value = wh
    list_column = ["p1", "p2", "p3", "p4", "s1", "s2", "s3", "s4", "q1", "q2", "q3", "q4", "i1", "i2", "i3", "i4", "pf1", "time"]

    p1_value = val["P1"]
    p2_value = val["P2"]
    p3_value = val["P3"]
    p4_value = val["P4"]
    q1_value = val["Q1"]
    q2_value = val["Q2"]
    try:
        q3_value = val["Q3"]
    except:
        q3_value = 0
    q4_value = val["Q4"]
    i1_value = val["I1"]
    i2_value = val["I2"]
    i3_value = val["I3"]
    i4_value = val["I4"]
    s1_value = val["S1"]
    s2_value = val["S2"]
    s3_value = val["S3"]
    s4_value = val["S4"]
    pf1_value = val["PF1"]
    p1_wh_value += val["P1_wh"]*3
    p2_wh_value += val["P2_wh"]*3
    p3_wh_value += val["P3_wh"]*3
    p4_wh_value += val["P4_wh"]*3
    if(keep_minute != unixtime_to_readable(time_value)[4]):
        list_val = []

        for col in d_1m_cur:
            if(col != "time"):          		
                list_val.append(round(mean(d_1m_cur[col]),2))
        # new > add append time_value
        list_val.append(time_value)
        d_1m = d_1m.append(pd.DataFrame([list_val], columns=list_column), ignore_index=True)
        d_1m_cur = pd.DataFrame()
        keep_minute = unixtime_to_readable(time_value)[4]

    if(unixtime_to_readable(time_value)[4] == "30" and check30 == True):
        print("30minutes")
        list_val = []
        for col in d_30m_cur:
            if(col != "time"):  
                list_val.append(round(mean(d_30m_cur[col]),2))
        # new > add append time_value
        list_val.append(time_value)
        d_30m = d_30m.append(pd.DataFrame([list_val], columns=list_column), ignore_index=True)
        d_30m_cur = pd.DataFrame()
        check30 = False
    elif(unixtime_to_readable(time_value)[4] != "30" and check30 == False):
        print("re value")
        check30 = True

    if(keep_hour != unixtime_to_readable(time_value)[3]):
        list_val_1hr = []
        for col in d_1hr_cur:
            if(col != "time"):  
                list_val_1hr.append(round(mean(d_1hr_cur[col]),2))
        # new > add append time_value
        list_val_1hr.append(time_value)
        d_1hr = d_1hr.append(pd.DataFrame([list_val_1hr], columns=list_column), ignore_index=True)

        d_1hr_cur = pd.DataFrame()

        list_val_30m = []
        for col in d_30m_cur:
            if(col != "time"):  
                list_val_30m.append(round(mean(d_30m_cur[col]),2))
        # new > add append time_value
        list_val_30m.append(time_value)
        d_30m = d_30m.append(pd.DataFrame([list_val_30m], columns=list_column), ignore_index=True)
        d_30m_cur = pd.DataFrame()
        keep_hour = unixtime_to_readable(time_value)[3]

    if(keep_day != unixtime_to_readable(time_value)[2]):
        print("change day")
        save_json(time_data, d_1m, d_30m, d_1hr, p1_wh_value, p2_wh_value, p3_wh_value, p4_wh_value, list_column)
        time_data = []
        d_1m, d_30m, d_1hr, d_1m_cur, d_30m_cur, d_1hr_cur = (pd.DataFrame() for i in range(6))
        p1_wh_value, p2_wh_value, p3_wh_value, p4_wh_value = (0 for i in range(4))
        keep_day = unixtime_to_readable(time_value)[2]

    time_data.append(time_value)
    list_values = [p1_value, p2_value, p3_value, p4_value, s1_value, s2_value, s3_value, s4_value,\
                    q1_value, q2_value, q3_value, q4_value, i1_value, i2_value, i3_value, i4_value, pf1_value, time_value]
    d_1m_cur = d_1m_cur.append(pd.DataFrame([list_values], columns=list_column), ignore_index=True)
    d_30m_cur = d_30m_cur.append(pd.DataFrame([list_values], columns=list_column), ignore_index=True)
    d_1hr_cur = d_1hr_cur.append(pd.DataFrame([list_values], columns=list_column), ignore_index=True)
    d = [d_1m, d_30m, d_1hr, d_1m_cur, d_30m_cur, d_1hr_cur]
    wh = [p1_wh_value, p2_wh_value, p3_wh_value, p4_wh_value]

    return(keep_day, keep_hour, keep_minute, check30, d, wh, time_data)


# th1 = threading.Thread(target = keep_data_realtime).start()
# th2 = threading.Thread(target = backup_from_firebase).start()
