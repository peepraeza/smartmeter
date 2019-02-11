#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from ..models import User
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

tz = pytz.timezone('Asia/Bangkok')
database_types = ['X', 'A', 'B', 'C']

# def send_pwd_mail(request):
    
    
def make_login(request):
    request.session["user"] = "hello"
    return HttpResponse("login completed")
    
def logout(request):
    if request.method == "POST":
        del request.session["user"]
        return redirect("/signin/")
    else:
        return redirect("/")
    
def signin(request):
    if request.method == "POST":
        if request.POST.get("send-mail") == "yes":
            admin = User.objects.get(username="admin")
            email = admin.email
            try:
                if admin.digest_pass != "":
                    massage = 'รหัสผ่านของคุณคือ {}'.format(admin.raw_password)
                else:
                    massage = 'คุณยังไม่ได้ตั้งรหัสผ่าน'
                send_mail(
                    "การกู้คืนรหัสผ่านสำหรับหน้าเว็บ Home Energix",
                    massage,
                    'sansara.farm.10@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, "signin.html", {"message": "ส่งอีเมลสำเร็จ"})
            except:
                return render(request, "signin.html", {"message": "การส่งอีเมลล้มเหลว"})
    return render(request, "signin.html")
    
def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST.get("username"))
            login_success = user._validate_password(request.POST.get("password"))
            if login_success:
                request.session["user"] = user.username
                return redirect("/")
            else:
                return render(request, "signin.html", {"message": "ชื่อผู้ใช้หรือรหัสผ่านผิด"})
        except:
            return render(request, "signin.html", {"message": "ชื่อผู้ใช้หรือรหัสผ่านผิด"})
    else:
        return redirect("/signin/")
    # return render(request, "signin.html")
    
def change_password(request):
    admin = User.objects.get(pk=1)
    oldpwd = request.POST.get("old-pass")
    newpwd = request.POST.get("new-pass")
    change_success = admin._change_password(oldpwd, newpwd)
    if change_success:
        return HttpResponse(json.dumps({
            "status": True,
        }))
    else:
        return HttpResponse(json.dumps({
            "status": False,
        }))
        
def change_email(request):
    admin = User.objects.get(pk=1)
    pwd = request.POST.get("pass")
    email = request.POST.get("email")
    change_success = admin._change_email(pwd, email)
    if change_success:
        return HttpResponse(json.dumps({
            "status": True,
        }))
    else:
        return HttpResponse(json.dumps({
            "status": False,
        }))