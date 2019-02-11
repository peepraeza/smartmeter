#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Meter
from ..post_data import parse_keys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from datetime import datetime, timedelta
import time
import requests
import pytz
import numpy as np
import os

tz = pytz.timezone('Asia/Bangkok')
database_types = ['X', 'A', 'B', 'C']

def edit_channel(request):
    ch = int(request.POST.get("m_ch"))
    des = request.POST.get("channel_description")
    _m = Meter.objects.filter(channel=ch).update(description=des)
    
    return redirect("/setting/")
    
def edit_ip(request):
    ip = request.POST.get("rp_ip")
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, '../../static/json/ip.txt')
    data_file = open(file_path , 'w')       
    ip = data_file.write(ip)
    return redirect("/setting/")
    
def edit_bill(request):
    bill = request.POST.get("cbill")
    unit = request.POST.get("unit")
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, '../../static/json/setting.json')
    data = {"bill-cycle": bill, "unit": unit}
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)     
    return redirect("/setting/")