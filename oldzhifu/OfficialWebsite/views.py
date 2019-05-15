# -*- coding=utf8 -*-
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,HttpResponse,redirect
from django.http.response import JsonResponse
from django.db import transaction
from .models import *
# Create your views here.


#首页
def index(request):
    ProductList = ProductType.objects.all()
    paginator = Paginator(ProductList, 4)
    ProductTypeList = paginator.page(1)

    #3603D全景 数据
    panoramas = ProductCenter.objects.filter(producttype__id=9).values()
    paginators = Paginator(panoramas, 4)
    ProductTypeLists = paginators.page(1)

    #合作公司数据
    panorama_1 = CompanyInformation.objects.all()
    paginator_1 = Paginator(panorama_1, 8)
    CompanyLists = paginator_1.page(1)

    #变形记
    change = Metamorphosis.objects.all()
    change_1 =  Paginator(change, 3)
    changeList = change_1.page(1)

    changes = Metamorphosis.objects.all()
    changes_1 =  Paginator(changes, 3)
    changesList = changes_1.page(1)
    return  render(request,'index.html',{"ProductTypeList":ProductTypeList,"ProductTypeLists":ProductTypeLists,"CompanyLists":CompanyLists,"changeList":changeList,"changesList":changesList})

#产品中心
def cplist(request):
    ids = request.GET.get('id')
    numberpages = int(request.GET.get("numberpages"))
    if numberpages == 0:
        numberpages = 1
    Typed = request.GET.get("Typed")
    #查询全部的商品类型
    ProductTypeList = ProductType.objects.all()
    if ids is None:
        ids = 1
    """""""""""""""""""""""""""""""""""""""分页"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #产品中心进入
    DefaultProductList = ProductCenter.objects.filter(producttype__id=1).values('name','path','producttype__id','id')
    # #根据ID  查询
    if Typed == "SelId":
        DefaultProductList = ProductCenter.objects.filter(producttype__id=ids).values('name','path','producttype__id','id')
    # #每页六条数据
    paginator = Paginator(DefaultProductList, 6.2)
    if Typed == "Add":
        numberpages =  int(numberpages) + 1
    if Typed == "Reduce":
            numberpages = int(numberpages) -1
    # #默认第一页or  显示第几页
    pageList = paginator.page(numberpages)
    # #总页数
    Count = paginator.num_pages
    CountList = []
    for  b in  range(Count):
        CountList.append(b+1)
    # #是否有上一页
    Previouspages = pageList.has_previous()
    # #是否有下一页
    Previouspage = pageList.has_next()
    #当前页数
    PageNnumber = pageList.number
    return render(request, 'cplist.html', {"ProductTypeList":ProductTypeList,"pageList": pageList,"CountList":CountList,"Previouspages":Previouspages,"Previouspage":Previouspage,"PageNnumber":PageNnumber,"DataId":ids})
#效果图详情页
def cpdetail(request):
    ids = request.GET.get("id")
    ProList =  ProductCenter.objects.filter(id=ids).values('path','path1','path2')
    return  render(request,"cpdetail.html",{"ProList":ProList})

#成功页面
def Success(request):
    return  render(request,'Success.html')

#需求
def Demand(request):
    data = {}
    type = request.POST['type']
    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    style = request.POST['style']
    noodlesproduct = request.POST['noodlesproduct']
    try:
        with transaction.atomic():
            if  type =='Foreman':
                demandtype='工长'
                DemandTable.objects.create(name=name,phone=phone,address=address,style=style,noodlesproduct=noodlesproduct,demandtype=demandtype)
                return redirect('Success.html')
            if type == 'Company':
                demandtype = '装修公司'
                count = DemandTable.objects.create(name=name, phone=phone, address=address, style=style,noodlesproduct=noodlesproduct, demandtype=demandtype)
                return redirect('Success.html')
    except Exception as err:
        return redirect('index.html')

    return redirect('index.html')





#关于我们
def about(request):
    return  render(request,"about.html")


#变形记
def newslist(request):
    numberpages = int(request.GET.get("numberpages"))
    Typed = request.GET.get("Typed")
    Met = Metamorphosis.objects.all()
    #每3条为一页
    paginator = Paginator(Met, 3.2)
    if Typed == "Add":
        numberpages = int(numberpages) + 1
    if Typed == "Reduce":
        numberpages = int(numberpages) - 1
    #显示第几页
    pageList = paginator.page(numberpages)
    # #总页数
    Count = paginator.num_pages
    CountList = []
    for b in range(Count):
        CountList.append(b + 1)
        # #是否有上一页
    Previouspages = pageList.has_previous()
    # #是否有下一页
    Previouspage = pageList.has_next()
    # 当前页数
    PageNnumber = pageList.number
    return  render(request,"newslist.html",{"pageList":pageList,"CountList":CountList,"Previouspages":Previouspages,"Previouspage":Previouspage,"PageNnumber":PageNnumber})



#变形记详情页
def newsdetail(request):
    ids = request.GET.get("id")
    MetaList =  Metamorphosis.objects.filter(id=ids).values()
    return  render(request,"newsdetail.html",{"MetaList":MetaList})



#联系我们
def contact(request):
    return  render(request,"contact.html")


#在线留言
def message(request):
    types = request.GET.get("type")
    if types == "Add":
        name = request.GET.get("name")
        phone = request.GET.get("phone")
        content = request.GET.get("content")
        Guestbook.objects.create(name=name,phone=phone,content=content)
        return render(request, 'Success.html')
    return  render(request,"message.html")

def DetailsCompany(request):
    numberpages = int(request.GET.get("numberpages"))
    Typed = request.GET.get("Typed")
    Com = CompanyInformation.objects.all()
    # 每3条为一页
    paginator = Paginator(Com, 3.2)
    if Typed == "Add":
        numberpages = int(numberpages) + 1
    if Typed == "Reduce":
        numberpages = int(numberpages) - 1
    # 显示第几页
    pageList = paginator.page(numberpages)
    # #总页数
    Count = paginator.num_pages
    CountList = []
    for b in range(Count):
        CountList.append(b + 1)
    Previouspages = pageList.has_previous()
    # #是否有下一页
    Previouspage = pageList.has_next()
    # 当前页数
    PageNnumber = pageList.number
    return render(request,"DetailsCompany.html",{"pageList":pageList,"CountList":CountList,"Previouspages":Previouspages,"Previouspage":Previouspage,"PageNnumber":PageNnumber})
