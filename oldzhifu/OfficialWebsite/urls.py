"""oldzhifu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from OfficialWebsite import  views

urlpatterns = [
    # url('admins/', admin.site.urls),
    url('index.html',views.index,name="index.html"),
    url('cplist.html', views.cplist, name="cplist.html"),
    url('cpdetail.html', views.cpdetail, name="cpdetail.html"),
    url('Demand', views.Demand, name="Demand"),
    url('Success.html/', views.Success, name="Success.html"),
    url('about.html/', views.about, name="about.html"),
    url('newslist.html/', views.newslist, name="newslist.html"),
    url('newsdetail.html/', views.newsdetail, name="newsdetail.html"),
    url('contact.html/', views.contact, name="contact.html"),
    url('message.html/', views.message, name="message.html"),
    #Details company
    url('DetailsCompany.html/', views.DetailsCompany, name="DetailsCompany.html"),
]
