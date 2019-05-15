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
from zhifu import views
urlpatterns = [
    url('admin/', admin.site.urls),
    url('needs_chose/', views.needs_chose),
    url('user_edit/', views.user_edit),
    url('user_designer/', views.user_designer),
    url('user_worker/', views.user_worker),
    url('designer/', views.designer),
    url('worker/', views.worker),
    url('designer_info/', views.designer_info),
    url('worker_info/', views.worker_info),
    url('topic/', views.topic),
    url('topic_info/', views.topic_info),
    url('change/', views.change),
    url('change_info/', views.change_info),
    url('comment/', views.comment),
    url('user/', views.user),
    url('user_info/', views.user_info),
    url('Change_Openid/',views.Change_Openid),
    url('comment_openid_update/',views.comment_openid_update),
    url('topic_openid_update/',views.topic_openid_update),
    url('ceshi_sel/',views.ceshi_sel),
    url('topic_add_comments/',views.topic_add_comments),
    url('user_add_fabulous/',views.user_add_fabulous),
    url('upd_Fans/',views.upd_Fans),
    url('comment_operation/',views.comment_operation),
    url("ceshi/",views.ceshi),
    url("SelOwner/",views.SelOwner),
    url("PictureMaking/",views.PictureMaking),
    url("TopicOfConversation/",views.TopicOfConversation),
    url("CommentAuthority/",views.CommentAuthority),
    url("AddDeformationMeter/",views.AddDeformationMeter),
    url('ShoppingCartsOperation',views.ShoppingCartsOperation),
    url('WeChatPayment/',include('WeChatPayment.urls')),
    url('OfficialWebsite/',include('OfficialWebsite.urls'))




]
