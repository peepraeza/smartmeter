from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

class AuthenticationChecking(object):
    def process_request(self, request):
        if(request.path not in ["/signin/", "/signin", "/makelogin/", "/makelogin", "/login/", "/login"]):
            if("user" not in request.session):
                return redirect("/signin/")
            else:
                return None
        else:
            return None
    
    def __call__(self, request):
        response = self.process_request(request)
        return response