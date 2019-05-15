# -*- coding=utf8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http.response import JsonResponse
from  .models import *
from django.db.models import Q
from django.db import transaction
import chardet
import base64
import re

# Create your views here.
#接收需求
def needs_chose(request):
    if request.method == "GET":
        address = request.GET.get('address')
        need = request.GET.get('need')
        xiaoqu = request.GET.get('xiaoqu')
        chenghu = request.GET.get('chenghu')
        lianxi = request.GET.get('lianxi')
        xuqiu = request.GET.get('xuqiu')
        huxing = request.GET.get('huxing')
        mianji = request.GET.get('mianji')
        housetype = request.GET.get('housetype')
        Needs.objects.create(need=need,
                                    address=address,
                                    xiaoqu=xiaoqu,
                                    chenghu=chenghu,
                                    lianxi=lianxi,
                                    xuqiu=xuqiu,
                                    huxing=huxing,
                                    mianji=mianji,
                                    housetype=housetype)

        return JsonResponse({"msg":"提交成功！"})

#用户信息修改（第一次提交保存信息，第二次提交修改信息）
def user_edit(request):
    print(request.method)
    # post请求，获取页面信息
    if request.method == "POST":
        openid = request.POST.get('openid')

        if Client.objects.filter(openid=openid):
            client = Client.objects.filter(openid=openid).values()
            data = {}
            data["list"] = list(client)
            return JsonResponse(data)
        else:
            return JsonResponse({'msg':'success'})
    # get请求，提交用户信息
    if request.method == 'GET':
        openid = request.GET.get('openid')
        name = request.GET.get('name')
        sex = request.GET.get('sex')
        age = request.GET.get('age')
        huxing = request.GET.get('huxing')
        mianji = request.GET.get('mianji')
        phone = request.GET.get('phone')
        # 判断是否为第一次提交
        if Client.objects.filter(openid=openid):
            # 修改信息
            obj = Client.objects.get(openid=openid)
            obj.name = name
            obj.sex = sex
            obj.age = age
            obj.huxing = huxing
            obj.mianji = mianji
            obj.phone = phone
            obj.save()
            return JsonResponse({"msg": "修改成功！"})
        else:
            # 创建新信息
            Client.objects.create(openid=openid,
                                        name=name,
                                        sex=sex,
                                        age=age,
                                        phone=phone,
                                        huxing=huxing,
                                        mianji=mianji
                                  )
            return JsonResponse({"msg":"创建成功！"})
# 申请工人
def user_worker(request):
    if request.method == "GET":
        openid = request.GET.get('openid')
        name = request.GET.get('name').encode('utf8')
        sex = request.GET.get('sex')
        age = request.GET.get('age')
        exp = request.GET.get('exp')
        baojia = request.GET.get('baojia')
        shenfenid = request.GET.get('shenfenid')
        phone = request.GET.get('phone')
        diqu = request.GET.get('diqu')
        jianshu = request.GET.get('jianshu').encode('utf8')
        fengge1 = request.GET.get('fengge1')
        fengge2 = request.GET.get('fengge2')
        # 验证用户唯一性
        if Worker.objects.filter(openid=openid):

            return JsonResponse({"msg": "请勿重复提交！"})
        else:
            Worker.objects.create(openid=openid,
                                         name=name,
                                         sex=sex,
                                         age=age,
                                         exp=exp,
                                         baojia=baojia,
                                         shenfenid=shenfenid,
                                         phone=phone,
                                         diqu=diqu,
                                         jianshu=jianshu,
                                         fengge1=fengge1,
                                         fengge2=fengge2)
            return JsonResponse({"msg":"提交成功！"})
# 申请设计师
def user_designer(request):
    if request.method == "GET":
        openid = request.GET.get('openid')
        print(openid)
        name = request.GET.get('name').encode('utf8')
        sex = request.GET.get('sex')
        age = request.GET.get('age')
        exp = request.GET.get('exp')
        baojia = request.GET.get('baojia')
        shenfenid = request.GET.get('shenfenid')
        phone = request.GET.get('phone')
        diqu = request.GET.get('diqu')
        jianshu = request.GET.get('jianshu').encode('utf8')
        fengge1 = request.GET.get('fengge1')
        # fengge2 = request.GET.get('fengge2')
        # 验证用户唯一性

        if Designer.objects.filter(openid=openid):
            return JsonResponse({"msg": "请勿重复提交！"})
        else:
            Designer.objects.create(openid=openid,
                                           name=name,
                                           sex=sex,
                                           age=age,
                                           exp=exp,
                                           baojia=baojia,
                                           shenfenid=shenfenid,
                                           phone=phone,
                                           diqu=diqu,
                                           jianshu=jianshu,
                                           fengge1=fengge1)
            return JsonResponse({"msg":"提交成功！"})

#请求设计师列表
def designer(request):
    # 请求个人设计师信息
    if request.GET.get('designer_id'):
        id = request.GET.get('designer_id')
        print(id)
        designer = Designer.objects.filter(id=id).values()
        data = {}
        data['list'] = list(designer)
        return JsonResponse(data)
    # 请求设计师列表信息
    if request.method == 'GET':
        data = {}
        designers = Designer.objects.order_by("id")
        print(designers)
        designers = designers.values()
        print(designers)
        data["list"] = list(designers)
        return JsonResponse(data)
    if request.method == 'POST':
        # 按照地区筛选
        diqu = request.POST.get('diqu')
        if diqu:
            data = {}
            designers = Designer.objects.filter(diqu=diqu)
            designers = designers.values()
            data["list"] = list(designers)
            return JsonResponse(data)
        xingji = request.POST.get('xingji')
        # 按照星级筛选
        if xingji:
            print(xingji)
            data = {}
            designers = Designer.objects.filter(xingji=xingji)
            designers = designers.values()
            data["list"] = list(designers)
            return JsonResponse(data)
        # 按照销量筛选
        xiaoliang = request.POST.get('xiaoliang')
        if xiaoliang:
            print (xiaoliang)
            # 默认按照ID排序
            if xiaoliang == '0':
                data = {}
                designers1 = Designer.objects.order_by("id")
                print(designers1)
                designers = designers1.values()
                print(designers)
                data["list"] = list(designers)
                return JsonResponse(data)
            # 销量从高到低排序
            if xiaoliang == "2":
                data = {}
                designers = Designer.objects.order_by("xiaoliang")
                designers = designers.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            # 销量从低到高排序
            if xiaoliang == '1':
                data = {}
                designers = Designer.objects.order_by("-xiaoliang")
                designers = designers.values()
                data["list"] = list(designers)
                return JsonResponse(data)
        # 按照报价筛选
        baojia = request.POST.get('baojia')
        if baojia:
            print (baojia)
            # 默认按照ID排序
            if baojia == '0':
                data = {}
                designers1 = Designer.objects.order_by("id")
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            # 报价从高到低排序
            if baojia == "2":
                data = {}
                designers = Designer.objects.order_by("baojia")
                designers = designers.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            # 报价从低到高排序
            if baojia == '1':
                data = {}
                designers = Designer.objects.order_by("-baojia")
                designers = designers.values()
                data["list"] = list(designers)
                return JsonResponse(data)
        # 按照职业筛选
        chose = request.POST.get('chose')
        if chose:
            print(chose)
            if chose == 'shinei':
                data = {}
                designers1 = Designer.objects.filter(fengge1='室内设计')
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'pingmian':
                data = {}
                designers1 = Designer.objects.filter(fengge1='平面改造')
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'xiaoguo':
                data = {}
                designers1 = Designer.objects.filter(fengge1='效果图绘制')
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'gongzhuang':
                data = {}
                designers1 = Designer.objects.filter(fengge1='工装设计')
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
# 设计师个人页面
def designer_info(request):
    print(request.method)
    # 获取设计师id
    if request.GET.get('id'):
        id= request.GET.get('id')
        # 获取设计师个人信息
        info = Designer.objects.filter(id=id).values()
        # 获取工人评分
        info_xingji = info[0].get("xingji")
        # 获取同行中评分低的
        designers = Designer.objects.filter(xingji__lt=info_xingji)
        num = len(designers)
        # 获取同行总数
        designers_all = Designer.objects.all()
        num_all = len(designers_all)
        data = {}
        data['list'] = list(info)
        data['num_all'] = num_all
        data['num'] = num
        return JsonResponse(data)
    if request.GET.get('openid'):
        openid = request.GET.get('openid')
        # 获取设计师个人信息
        info = Designer.objects.filter(openid=openid).values()
        # 获取工人评分
        info_xingji = info[0].get("xingji")
        print(info_xingji)
        # 获取同行中评分低的
        designers = Designer.objects.filter(xingji__lt=info_xingji)
        num = len(designers)
        # 获取同行总数
        designers_all = Designer.objects.all()
        num_all = len(designers_all)
        data = {}
        data['list'] = list(info)
        data['num_all'] = num_all
        data['num'] = num
        return JsonResponse(data)

# 请求工人列表
def worker(request):
    if request.method == 'GET':
        data = {}
        workers = Worker.objects.order_by("id").values()
        data["list"] = list(workers)
        return JsonResponse(data)
    if request.method == 'POST':
        # 按照地区筛选
        diqu = request.POST.get('diqu')
        print(request.POST)
        print(diqu)
        if diqu:
            data = {}
            workers = Worker.objects.filter(diqu=diqu).values()
            data["list"] = list(workers)
            return JsonResponse(data)
        xingji = request.POST.get('xingji')
        xingji2=request.POST.get('xingji2')
        # 按照星级筛选
        if xingji:
            print(xingji)
            data = {}
            workers = Worker.objects.filter(Q(xingji=xingji)| Q(xingji=xingji2)).values()
            data["list"] = list(workers)
            return JsonResponse(data)
        # 按照销量筛选
        xiaoliang = request.POST.get('xiaoliang')
        if xiaoliang:
            print (xiaoliang)
            # 默认按照ID排序
            if xiaoliang == '0':
                data = {}
                workers = Worker.objects.order_by("id").values()
                data["list"] = list(workers)
                return JsonResponse(data)
            # 销量从高到低排序
            if xiaoliang == "2":
                data = {}
                workers = Worker.objects.order_by("xiaoliang").values()
                data["list"] = list(workers)
                return JsonResponse(data)
            # 销量从低到高排序
            if xiaoliang == '1':
                data = {}
                workers = Worker.objects.order_by("-xiaoliang").values()
                data["list"] = list(workers)
                return JsonResponse(data)
        # 按照报价筛选
        baojia = request.POST.get('baojia')
        if baojia:
            print (baojia)
            # 默认按照ID排序
            if baojia == '0':
                data = {}
                designers1 = Worker.objects.order_by("id")
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            # 报价从高到低排序
            if baojia == "2":
                data = {}
                workers = Worker.objects.order_by("baojia").values()
                data["list"] = list(workers)
                return JsonResponse(data)
            # 报价从低到高排序
            if baojia == '1':
                data = {}
                workers = Worker.objects.order_by("-baojia").values()
                data["list"] = list(workers)
                return JsonResponse(data)
        # 按照职业筛选
        chose = request.POST.get('chose')
        if chose:
            print(chose)
            if chose == 'chaiza':
                data = {}
                designers1 = Worker.objects.filter(Q(fengge1='拆砸工')| Q(fengge2='拆砸工'))
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'shuidian':
                data = {}
                designers1 = Worker.objects.filter(Q(fengge1='水电工')| Q(fengge2='水电工'))
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'yangtai':
                data = {}
                designers1 = Worker.objects.filter(Q(fengge1='封阳台')| Q(fengge2='封阳台'))
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'niwa':
                data = {}
                designers1 = Worker.objects.filter(Q(fengge1='泥瓦工')| Q(fengge2='泥瓦工'))
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'youqi':
                data = {}
                designers1 = Worker.objects.filter(Q(fengge1='油漆工')| Q(fengge2='油漆工'))
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'mugong':
                data = {}
                designers1 = Worker.objects.filter(Q(fengge1='木工')| Q(fengge2='木工'))
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
            if chose == 'baojie':
                data = {}
                designers1 = Worker.objects.filter(Q(fengge1='保洁工')| Q(fengge2='保洁工'))
                designers = designers1.values()
                data["list"] = list(designers)
                return JsonResponse(data)
# 工人个人页面
def worker_info(request):
    print(request.method)
    # 获取工人id
    worker_id = request.GET.get('id')
    # 获取个人信息
    info = Worker.objects.filter(id=worker_id).values()
    print(info)
    # 获取工人评分
    info_xingji = info[0].get("xingji")
    print(info_xingji)
    # 获取同行中评分低的
    workers = Worker.objects.filter(xingji__lt=info_xingji)
    num = len(workers)
    print(num)
    # 获取同行总数
    workers_all = Worker.objects.all()
    num_all = len(workers_all)
    data = {}
    # data中添加数据
    data['list'] = list(info)
    data['num_all'] = num_all
    data['num'] = num
    return JsonResponse(data)

# 话题列表
def topic(request):
    if request.method == 'GET':
        data = {}
        # 获取话题列表
        topics = Topic.objects.order_by('id').values()
        print(topics)
        data["list"] = list(topics)
        return JsonResponse(data)

# 话题页面
def topic_info(request):
    # 获取话题id
    topic_id = request.GET.get('id')
    # print(topic_id)
    # 获取话题内容
    info = Topic.objects.filter(id=topic_id).values()
    print("===================================>")
    info_list = Topic.objects.get(id=topic_id).comment.all()

    print(info_list)
    commentsList = info_list.values()
    # data添加数据
    data = {}
    data['list'] = list(info)
    data['info_list']=list(commentsList)
    return JsonResponse(data)

# 变形记列表页
def change(request):
    # print(request.method)
    # 获取变形记列表
    changes = Change.objects.order_by('id').values('id','title','date','img1','huxing','mianji','huafei','weizhi','img1','designer__name','designer__touxiang','test1')
    for i in changes:
        print(i)
    data = {}
    data['list'] = list(changes)
    return JsonResponse(data)


# 变形记页面
def change_info(request):
    # 获取变形记id
    change_id = request.GET.get('id')
    # 获取变形计信息
    info = Change.objects.filter(id=change_id).values()
    # 获取变形记的设计师
    designer_id = info[0].get('designer_id')
    designer = Designer.objects.filter(id=designer_id).values()
    # 获取变形记的评论(内容、时间)
    print("======================")
    comment_obj =Change.objects.get(id=change_id).comment.all()
    print(comment_obj)
    comments = comment_obj.values()

    data = {}
    data["list"] = list(info)
    data["designer"] = list(designer)
    data["comment"] = list(comments)
    return JsonResponse(data)
# 评论
def comment(request):
    # 点赞
    if request.GET.get('dianzan'):
        dianzan = request.GET.get('dianzan')

    # 获取评论内容
    test = request.GET.get('test')
    openid = request.GET.get('openid')
    changeid =request.GET.get('changeid')
    name = request.GET.get("name")
    # 将评论写入数据库
    Comment.objects.create(name=name, openid=openid, test=test)
    comment = Comment.objects.filter(test=test).values()
    commentid = comment[0].get('id')

    # 创建评论与变形计的关联
    obj = Change.objects.get(id=changeid)
    obj.comment.add(commentid)
    data = {"msg":'评论成功'}
    return JsonResponse(data)

# 所有微信用户
def user(request):
    name = request.GET.get('name')
    img = request.GET.get('img')
    openid = request.GET.get('openid')
    city = request.GET.get('city')
    # 判断用户是否为第一次登陆
    if User.objects.filter(openid=openid):
        return JsonResponse({"msg": "欢迎再次登陆"})
    else:
        # 用户基本信息写入数据库
        User.objects.create(name=name,
                                   city=city,
                                   openid=openid,
                                   img=img)
        return JsonResponse({"msg":'登陆成功'})
# 用户个人页面
def user_info(request):
    print(request.method)
    openid = request.GET.get('openid')
    # 判断用户身份,获取信息
    # 设计师身份
    if Designer.objects.filter(openid=openid):
        info = Designer.objects.filter(openid=openid).values()
        print(info)
        data = {}
        data['list'] = list(info)
        return JsonResponse(data)
    # 工人身份
    elif Worker.objects.filter(openid=openid):
        info = Worker.objects.filter(openid=openid).values()
        print(info)
        data = {}
        data['list'] = list(info)
        return JsonResponse(data)
    # 普通用户身份
    else:
        return JsonResponse({"msg": '该用户没有主页'})
    # 获取微信用户信息
    # info = User.objects.filter(openid=openid).values()

def Change_Openid(request):
    openid = request.GET.get("openid")
    shuju = Change.objects.filter(designer__openid=openid).values()
    data = {}
    data['list'] = list(shuju)
    return JsonResponse(data)

#通过评论openid 和 topic__id 修改点赞数量和状态
def comment_openid_update(request):
    openid = request.GET.get("openid")
    topicId = request.GET.get("topicid")
    dianzan = request.GET.get("dianzan")
    dianzanfunc = request.GET.get("dianzanfunc")
    openid_update=Comment.objects.filter(openid=openid,id=topicId).update(dianzan=dianzan,dianzanfunc=dianzanfunc)
    if openid_update>0:
        data = {"msg": '成功'}
        return JsonResponse(data)
    else:
        return  HttpResponse("失败")

#修改话题点赞
def topic_openid_update(request):
    openid = request.GET.get("openid")
    topicId = request.GET.get("topicid")
    dianzan = request.GET.get("dianzan")
    dianzanfunc = request.GET.get("dianzanfunc")
    openid_update = Comment.objects.filter(openid=openid,id=topicId).update(dianzan=dianzan,dianzanfunc=dianzanfunc)
    if openid_update>0:
        data = {"msg": '成功'}
        return JsonResponse(data)
    else:
        data = {"msg": '成功'}
        return JsonResponse(data)

#添加一条话题评论
def topic_add_comments(request):
    # 点赞
    if request.GET.get('dianzan'):
        dianzan = request.GET.get('dianzan')

    # 获点赞信息
    test = request.GET.get('test')
    openid = request.GET.get('openid')
    changeid = request.GET.get('changeid')
    name = request.GET.get('name').encode('utf8')
    # 将点赞写入数据库
    Comment.objects.create(name=name, openid=openid, test=test)
    comment = Comment.objects.filter(test=test).values()
    commentid = comment[0].get('id')

    # 创建评论与话题的关联
    ceshi = Topic.objects.get(id=changeid)
    ceshi.comment.add(commentid)
    data = {"msg": '评论成功'}
    return JsonResponse(data)

#获取我的变形记
def ceshi_sel(request):
    openid = request.GET.get("openid")
    shuju = Change.objects.filter(designer__openid='1544sfes').values()
    data = {}
    data['list'] = list(shuju)
    return JsonResponse(data)


#关注信息
def user_add_fabulous(request):
    type = request.GET.get("types")
    openid = request.GET.get("openid")
    #添加一个设计师的关注
    if type == 'Designer':
        designer_id = request.GET.get("designer_id")
        user = User.objects.filter(openid=openid).first()
        #添加用户跟设计师关联
        user.designers.add(designer_id)
        data = {"msg": '添加成功'}
        return JsonResponse(data)

    #添加一个工人的关注
    if type == 'Worker':
        worker_id = request.GET.get("worker_id")
        user = User.objects.filter(openid=openid).first()
        user.workers.add(worker_id)
        data = {"msg": '添加成功'}
        return JsonResponse(data)

    # #查询所有的关注记录
    if type == 'Sel':
        #查询关于设计师的关注
        designer_list =Designer.objects.filter(user__openid=openid).values()
        #查询关于工人的关注
        worker_list = Worker.objects.filter(user__openid=openid).values()
        data = {}
        data['designer_list'] = list(designer_list)
        data['worker_list'] = list(worker_list)
        return JsonResponse(data)

    #查询收藏的变形记跟话题
    if type == 'SelCollection':
        #openid
        topic_list = Topic.objects.filter(user__openid=openid).values()
        change_list = Change.objects.filter(user__openid=openid).values()
        data = {}
        data['topic_list'] = list(topic_list)
        data['change_list'] = list(change_list)
        return JsonResponse(data)

    #添加收藏记录
    if type == 'AddCollection':
        type_id = request.GET.get("type_id")
        #添加一条话题收藏数据
        if type_id == 'Topic_add':
            topics_id = request.GET.get("topics_id")
            users = User.objects.get(openid=openid)
            users.topicsFky.add(topics_id)
            data = {"msg": '添加成功'}
            return JsonResponse(data)
        #添加一条变形记收藏
        elif type_id == 'Change_add':
            topics_id = request.GET.get("topics_id")
            users = User.objects.get(openid=openid)
            users.changesFky.add(topics_id)
            data = {"msg": '添加成功'}
            return JsonResponse(data)


    #根据id和openid查询关注记录
    if type == 'SelIdCollection':
        type_id = request.GET.get("type_id")
        #根据id查询工人，是否有关注
        if type_id == 'Worker_sel':
            Workers_id = request.GET.get("Workers_id")
            workers_list = Worker.objects.filter(user__openid=openid, id=Workers_id).values()
            data = {}
            data['user_list'] = list(workers_list)
            return JsonResponse(data)

        #根据id查询设计师，是否有关注
        if type_id == 'Designer_sel':
            Designers_id = request.GET.get("gners_id")
            designer_list = Designer.objects.filter(user__openid=openid,id=Designers_id).values()
            data = {}
            data['user_list'] = list(designer_list)
            return JsonResponse(data)
        #根据id查询,是否有话题收藏记录
        if type_id == 'Topic_sel':
            Topics_id =request.GET.get("Topics_id")
            Topics_list = Topic.objects.filter(user__openid=openid,id=Topics_id).values()
            data = {}
            data['topics_list'] = list(Topics_list)
            return JsonResponse(data)
        #根据id查询，是否有变形记收藏记录
        if type_id =='Change_sel':
            Changes_id = request.GET.get("Changes_id")
            Changes_list = Change.objects.filter(user__openid=openid,id=Changes_id).values()
            data = {}
            data['changes_list'] = list(Changes_list)
            return JsonResponse(data)
    #根据id删除关注记录
    if type == 'del_Designer':
        designers_id = request.GET.get("designers_id")
        use = User.objects.filter(openid=openid).first()
        use.designers.remove(designers_id)
        data = {"msg": '删除成功'}
        return JsonResponse(data)

    if type == 'del_Worker':
        workers_id = request.GET.get("workers_id")
        use = User.objects.filter(openid=openid).first()
        use.workers.remove(workers_id)
        data = {"msg": '删除成功'}
        return JsonResponse(data)

    #根据openid和话题id删除，话题收藏
    if type == 'del_Topic':
        Topics_id =  request.GET.get("Topics_id")
        use = User.objects.filter(openid=openid).first()
        use.topicsFky.remove(Topics_id)
        data = {"msg": '删除成功'}
        return JsonResponse(data)
    #根据openid和变形记id删除，变形记收藏
    if type =='del_Change':
        Change_id = request.GET.get("Change_id")
        use = User.objects.filter(openid=openid).first()
        use.changesFky.remove(Change_id)
        data = {"msg": '删除成功'}
        return JsonResponse(data)


def upd_Fans(request):
    type =request.GET.get("types")
    GuanZhu = request.GET.get("GuanZhu")
    currency_id = request.GET.get("currency_id")
    xiaoliang = request.GET.get("xiaoliang")
    #修改设计师的关注量
    if type == 'Designer_Fans':
        Num = Designer.objects.filter(id=currency_id).update(guanzhu=GuanZhu)
        if Num>0:
            data = {"msg": '添加成功'}
            return JsonResponse(data)
        else:
            data = {"msg": '添加失败'}
            return JsonResponse(data)
    #修改工人的关注量
    if type == 'Worker_Fans':
        Num = Worker.objects.filter(id=currency_id).update(guanzhu=GuanZhu)
        if Num>0:
            data = {"msg": '添加成功'}
            return JsonResponse(data)
        else:
            data = {"msg": '添加失败'}
            return JsonResponse(data)

    #修改工人的销售量
    if type =="Worker_Sale":
        Num = Worker.objects.filter(id=currency_id).update(xiaoliang=xiaoliang)
        if Num>0:
            data = {"msg": '修改成功'}
            return JsonResponse(data)
        else:
            data = {"msg": '修改失败'}
            return JsonResponse(data)
    #修改设计师的销量
    if type =="Designer_Sale":
        Num = Designer.objects.filter(id=currency_id).update(xiaoliang=xiaoliang)
        if Num>0:
            data = {"msg": '修改成功'}
            return JsonResponse(data)
        else:
            data = {"msg": '修改失败'}
            return JsonResponse(data)
        return  HttpResponse("成功")


#评论表的操作
def comment_operation(request):
    type = request.GET.get("types")
    #根据id查询工人的评论
    if type =='Sel_Worker':
        workers_id = request.GET.get("workers_id")
        workers_list = Comment.objects.filter(worker__id=workers_id).values()
        data = {}
        data['list'] = list(workers_list)
        return JsonResponse(data)

    #根据id查询设计师的评论
    if type == 'Sel_Designer':
        designers__id = request.GET.get("designers__id")
        designers_list = Comment.objects.filter(designer__id=designers__id).values()
        data = {}
        data['list'] = list(designers_list)
        return JsonResponse(data)

    #添加评论
    if type == 'Add_comment':
        name =request.GET.get("name")
        openid = request.GET.get("openid")
        test = request.GET.get("test")
        type_id = request.GET.get("type_id")
        Magic_id = request.GET.get("Magic_id")
        #添加工人评论
        if type_id == "Worker":
            try:
                with transaction.atomic():
                    Comment.objects.create(name=name, openid=openid, test=test)
                    id = Comment.objects.filter(test=test).first()
                    wolis = Worker.objects.filter(id=Magic_id).first()
                    wolis.worker_evaluation.add(id.id)
                    data = {"msg": '添加成功'}
                    return JsonResponse(data)
            except Exception as err:
                return JsonResponse({'statuscode': '09'})
            else:
                return JsonResponse({'statuscode': '202'})
         #设计师评论
        if type_id == 'Designer':
            try:
                with transaction.atomic():
                    Comment.objects.create(name=name, openid=openid, test=test)
                    id = Comment.objects.filter(test=test).first()
                    wolis = Designer.objects.filter(id=Magic_id).first()
                    wolis.designer_evaluation.add(id.id)
                    data = {"msg": '添加成功'}
                    return JsonResponse(data)
            except Exception as err:
                return JsonResponse({'statuscode': '409'})
            else:
                return JsonResponse({'statuscode': '202'})

#订单表的操作
def ShoppingCartsOperation(request):
    #模式类型
    types = request.GET.get("types")
    #功能类型
    type_id = request.GET.get("type_id")
    #订单编号  后台生成
    import random
    import string
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 15))
    order_number = request.GET.get("order_number")
    #用户openid
    openid = request.GET.get("openid")
    #购买天数
    days_num = request.GET.get("days_num")
    #订单状态
    order_status =request.GET.get("order_status")
    #下单时间
    purchase_date =request.GET.get("purchase_date")
    #订单金额
    total_price = request.GET.get("total_price")
    #订单id
    ids = request.GET.get("id")
    #查询订单
    if types == "Sel":
        #查看全部订单
        if type_id == "all":
            user_list = Shopping_Cart.objects.filter(Q(openid=openid) | Q(worker_relationship__openid=openid) | Q(designer_relationship__openid=openid) ).values()
            data = {}
            data['list'] = list(user_list)
            return JsonResponse(data)

        #跟订单状态查询
        if type_id == "state":
            user_list = Shopping_Cart.objects.filter(Q(openid=openid) | Q(worker_relationship__openid=openid) | Q(designer_relationship__openid=openid) ,order_status=order_status).values()
            data = {}
            data['list'] = list(user_list)
            return JsonResponse(data)

        #查询订单里得工人信息
        if type_id == 'worker':
            worker_list = Worker.objects.filter(shopping_cart__openid=openid,shopping_cart__id=ids).values()
            data = {}
            data['worker_list'] = list(worker_list)
            return JsonResponse(data)
        #通过openid 判断 是否改订单的工人 或者 设计师,来判断是否拥有收款权限
        if type_id =="identity":
            worker_openid = request.GET.get("worker_openid")
            designer_openid = request.GET.get("designer_openid")
            if worker_openid:
                worker_list = Shopping_Cart.objects.filter(id=ids,order_number=order_number,worker_relationship__openid=openid).values()
                data = {}
                data["worker_list"] = list(worker_list)
                return JsonResponse(data)
            if designer_openid:
                designer_list =  Shopping_Cart.objects.filter(id=ids,order_number=order_number,designer_relationship__openid=openid).values()
                data = {}
                data["designer_list"] = list(designer_list)
                return JsonResponse(data)
        #查询订单里得设计师信息
        if type_id == "designer":
            designer_list = Designer.objects.filter(shopping_cart__openid=openid,shopping_cart__id=ids).values()
            data = {}
            data['designer_list'] = list(designer_list)
            return JsonResponse(data)

        if type_id == "ForeignKey":
            workers_id = request.GET.get("workers_id")
            designers_id =request.GET.get("designers_id")
            if workers_id != None:
                ShoppingcCart_list = Shopping_Cart.objects.filter(openid=openid,worker_relationship__id=workers_id, order_status=order_status).values()
                data = {}
                data['ShoppingcCart_list'] = list(ShoppingcCart_list)
                return JsonResponse(data)
            elif designers_id != None:
                ShoppingcCart_list = Shopping_Cart.objects.filter(openid=openid, designer_relationship__id=designers_id,
                                                                  order_status=order_status)
                data = {}
                data['ShoppingcCart_list'] = list(ShoppingcCart_list)
                return JsonResponse(data)
            else:
                data = {"msg": '401'}
                return JsonResponse(data)
    #添加订单
    if types =="Add":
        try:
            with transaction.atomic():
                Scart=Shopping_Cart.objects.create(order_number=salt,openid=openid,total_price=total_price)
                #添加工人订单
                if type_id == "Worker":
                    #获取工人id号
                    worker_id = request.GET.get("worker_id")
                    Scart.worker_relationship.add(worker_id)
                    data = {"msg": '添加工人订单成功'}
                    return JsonResponse(data)
                #添加设计师订单
                if type_id == "Designer":
                    designer_id = request.GET.get("designer_id")
                    Scart.designer_relationship.add(designer_id)
                    data = {"msg": '添加设计师订单成功'}
                    return JsonResponse(data)
        except Exception as err:
            return JsonResponse({'statuscode': '409'})
        else:
            return JsonResponse({'statuscode': '202'})
    #修改订单
    if types == "Upd":
        user_list = Shopping_Cart.objects.filter(openid=openid, id=ids)
        try:
            with transaction.atomic():
                if type_id == "OrderStatus":
                    user_list.update(order_status=order_status)
                    data = {"msg": '订单状态修改成功'}
                    return JsonResponse(data)
                if type_id == "Workers_Days":
                    user_list.update(days_num=days_num)
                    data = {"msg": '工人天数修改成功'}
                    return JsonResponse(data)
        except Exception as err:
            return JsonResponse({'statuscode': '409'})
        else:
            return JsonResponse({'statuscode': '202'})
    #删除订单
    if types == "Del":
        ShoppingcCart_list = Shopping_Cart.objects.filter(openid=openid,id=ids)
        #根据工人id删除订单
        if type_id == "Worker":
            workers_id = request.GET.get("workers_id")
            ShoppingcCart_list.worker_relationship.remove(workers_id)
            data = {"msg": '订单删除成功'}
            return JsonResponse(data)

        #根据设计师id删除订单
        if type_id == "Designer":
            designers_id = request.GET.get("designers_id")
            ShoppingcCart_list.designer_relationship.remove(designers_id)
            data = {"msg": '订单删除成功'}
            return JsonResponse(data)

        #删除全部
        if type_id == "None":
            ShoppingcCart_list.delete()
            data = {"msg": '订单删除成功'}
            return JsonResponse(data)


def ceshi(request):
    a = request.FILES.get("file")
    name = request.POST.get('imgname')
    pic = a.read()
    with open('static/'+name+'.jpg','wb') as f:
        f.write(pic)
    return  HttpResponse("成功")


def SelOwner(request):
    openid = request.GET.get("openid")
    #顾客查询
    OwnLisr = Client.objects.filter(openid=openid)
    #设计师查询
    DesLisr = Designer.objects.filter(openid=openid)
    #工人查询
    WorList = Worker.objects.filter(openid=openid)
    num = OwnLisr.__len__()
    num1 = DesLisr.__len__()
    num2 =WorList.__len__()
    if num1>0:
        data = {"msg": '202'}
        return JsonResponse(data)
    if num>0 or num2>0:
        data = {"msg": '200'}
        return JsonResponse(data)
    else:
        data = {"msg": '404'}
        return JsonResponse(data)


#评论权限
def CommentAuthority(request):
    openid = request.GET.get("openid")
    workId = request.GET.get("workId")
    desiId = request.GET.get("desiId")
    if workId:
       WorkCart = Shopping_Cart.objects.filter(openid=openid,worker_relationship__id=workId).all()
       num = WorkCart.__len__()
       if num>0:
            data = {"msg": '200'}
            return JsonResponse(data)
    if desiId:
        DesiCart = Shopping_Cart.objects.filter(openid=openid,designer_relationship__id=desiId).all()
        num1 = DesiCart.__len__()
        if num1>0:
            data = {"msg": '200'}
            return JsonResponse(data)
    else:
           data = {"msg": '404'}
           return JsonResponse(data)



#添加变形记
def AddDeformationMeter(request):
    openid = request.GET.get("openid")
    if openid:
        DesList = Designer.objects.filter(openid=openid).values()
        #获取到id
        id = DesList[0].get("id")
    #标题
    title = request.GET.get("title")
    #变形记内容
    test1 = request.GET.get("test1")
    #变形记首页面
    img1 = request.GET.get("img1")
    #户型
    huxing = request.GET.get("huxing")
    #面积
    mianji = request.GET.get("mianji")
    #花费
    huafei = request.GET.get("huafei")
    #位置
    weizhi = request.GET.get("weizhi")
    #房屋位置
    test2 = request.GET.get("test2")
    img2_1 = request.GET.get("img2_1")
    img2_2 = request.GET.get("img2_2")

    #房屋位置_1
    test3 = request.GET.get("test3")
    img3_1 = request.GET.get("img3_1")
    img3_2 = request.GET.get("img3_2")

    #房屋位置_2
    test4 = request.GET.get("test4")
    img4_1 = request.GET.get("img4_1")
    img4_2 =request.GET.get("img4_2")

    #房屋位置_3
    test5 = request.GET.get("test5")
    img5_1 = request.GET.get("img5_1")
    img5_2 =request.GET.get("img5_2")

    #房屋位置_4
    test6 = request.GET.get("test6")
    img6_1 = request.GET.get("img6_1")
    img6_2 =request.GET.get("img6_2")

    types = request.GET.get("type")

    if types =="AddTest":
       ChaNum = Change.objects.create(
            title=title,
            test1=test1,
            huxing=huxing,
            mianji=mianji,
            huafei=huafei,
            weizhi=weizhi,
            test2=test2,
            test3=test3,
            test4=test4,
            test5=test5,
            test6=test6,
            designer_id=id
        )
       if ChaNum.id  >0:
        data = {"msg": '200',"Change_id":ChaNum.id}
        return JsonResponse(data)

    if types =="UpdTest":
        Cha_id = request.GET.get("Cha_id")
        ChaNum = Change.objects.filter(designer__openid=openid,id=Cha_id).update(
            img1=img1,
            img2_1=img2_1,
            img2_2=img2_2,
            img3_1=img3_1,
            img3_2=img3_2,
            img4_1=img4_1,
            img4_2=img4_2,
            img5_1=img5_1,
            img5_2=img5_2,
            img6_1=img6_1,
            img6_2=img6_2,
        )
        if ChaNum>0:
            data = {"msg": '200'}
            return JsonResponse(data)
        else:
            data = {"msg": '404'}
            return JsonResponse(data)

    data = {"msg": '404'}
    return JsonResponse(data)


#把图片写入到项目中
def PictureMaking(request):
    a = request.FILES.get("file")
    print(a)
    name = request.POST.get('imgname')
    print(name)
    pic = a.read()
    with open('static/' + name, 'wb') as f:
        f.write(pic)
    data = {"msg": '200'}
    return JsonResponse(data)



#添加话题
def TopicOfConversation(request):
    title = request.GET.get("title")
    image1 = request.GET.get("image1")
    text1 = request.GET.get("text1")
    image2 = request.GET.get("image2")
    text2 = request.GET.get("text2")
    image3 = request.GET.get("image3")
    text3 = request.GET.get("text3")
    image4 =request.GET.get("image4")
    text4 =request.GET.get("text4")
    image5 =request.GET.get("image5")
    text5 =request.GET.get("text5")
    image6 =request.GET.get("image6")
    text6 =request.GET.get("text6")
    types = request.GET.get("type")
    if types == "AddTest":
      TopNum =  Topic.objects.create(
          title=title,
          text1=text1,
          text2=text2,
          text3=text3,
          text4=text4,
          text5=text5,
          text6=text6
        )
      if TopNum.id>0:
            data = {"msg": '200',"Topic_id":TopNum.id}
            return JsonResponse(data)
    if types == "UpdTest":
        Top_id = request.GET.get("Cha_id")
        TopNum = Topic.objects.filter(id=Top_id).update(
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            image5=image5,
            image6=image6
        )
        print(TopNum)
        if TopNum > 0:
            data = {"msg": '200'}
            return JsonResponse(data)
    data = {"msg": '400'}
    return JsonResponse(data)


    