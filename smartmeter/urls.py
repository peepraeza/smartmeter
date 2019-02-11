"""smartfarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import views, user_views, setting_views

urlpatterns = [
    # common views
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index', views.index),
    url(r'^setting/', views.setting),
    url(r'^graph/', views.graph),
    url(r'^history/', views.history),
    url(r'^delete_history/', views.del_history),

    # setting views
    url(r'^edit_channel/', setting_views.edit_channel),
    url(r'^edit_ip/', setting_views.edit_ip),
    url(r'^edit_bill/', setting_views.edit_bill),

    # user views
    url(r'^signin/', user_views.signin),
    url(r'^login/', user_views.login),
    url(r'^makelogin/', user_views.make_login),
    url(r'^logout/', user_views.logout),
    url(r'^user/change_password/', user_views.change_password),
    url(r'^user/change_email/', user_views.change_email),


]
