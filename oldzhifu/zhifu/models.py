# -*- coding=utf8 -*-
from django.db import models

# 定义用户类(微信用户)
class User(models.Model):
    openid = models.CharField(max_length=100)
    name = models.CharField(max_length=500, verbose_name='姓名')
    img = models.CharField(null=True, max_length=500, verbose_name='头像')
    city = models.CharField(max_length=32)

    #与设计师表创建关联
    designers = models.ManyToManyField(to='Designer')
    #与工人表创建关联
    workers = models.ManyToManyField(to='Worker')
    #与变形记表创建关联
    changesFky = models.ManyToManyField(to='Change')
    #与话题表创建关联
    topicsFky = models.ManyToManyField(to='Topic')

#定义客户类
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=100, verbose_name="唯一认证")
    name = models.CharField(max_length=4, verbose_name="客户姓名")
    sex = models.CharField(max_length=10, verbose_name='性别')
    age = models.CharField(max_length=2, verbose_name='年龄')
    huxing = models.CharField(null = True, max_length=32, verbose_name='户型')
    mianji = models.CharField(null = True, max_length=32, verbose_name='面积')
    phone = models.CharField(max_length=11,verbose_name='手机号')


    def __unicode__(self):
        return self.name

#定义设计师类
class Designer(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=100)
    touxiang = models.ImageField(null = True, blank=True, upload_to='static')
    name = models.CharField(max_length=4, verbose_name="设计师姓名")
    sex = models.CharField(max_length=10, verbose_name='性别')
    age = models.CharField(max_length=2, verbose_name='年龄')
    exp = models.CharField(max_length=2, verbose_name='从业经验')
    baojia = models.FloatField(max_length=8, default='100.00', verbose_name='报价')
    shenfenid = models.CharField(max_length=18, verbose_name='身份证')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    diqu = models.CharField(max_length=11, verbose_name='服务地区')
    jianshu = models.CharField(max_length=200, verbose_name='简述')
    fengge1 = models.CharField(max_length=11, verbose_name='风格1')
    xingji = models.FloatField(max_length=3, default=5, verbose_name='星级')
    xiaoliang = models.IntegerField(default=1, verbose_name='服务量')
    guanzhu = models.IntegerField(default=11, verbose_name='关注度')
    image1 = models.ImageField(null=True, blank=True, verbose_name='代表作1')
    image2 = models.ImageField(null=True, blank=True, verbose_name='代表作2')
    image3 = models.ImageField(null=True, blank=True, verbose_name='代表作3')
    # 收藏变形记
    # shoucang = models.ManyToManyField(to='Change', verbose_name='收藏变形记')

    #创建设计师和评论关系
    designer_evaluation = models.ManyToManyField(to="Comment")



    #创建设计

    def __unicode__(self):
        return self.name

    def __str__(self):
        return  self.name

#定义工人类
class Worker(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=100)
    touxiang = models.ImageField(max_length=32, null= True, upload_to='static')
    name = models.CharField(max_length=4, verbose_name="工人姓名")
    sex = models.CharField(max_length=10, verbose_name='性别')
    age = models.CharField(max_length=2, verbose_name='年龄')
    exp = models.CharField(max_length=2, verbose_name='从业经验')
    baojia = models.FloatField(max_length=8, default='100.00', verbose_name='报价')
    shenfenid = models.CharField(max_length=18, verbose_name='身份证')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    diqu = models.CharField(max_length=11, verbose_name='服务地区')
    jianshu = models.CharField(max_length=30, verbose_name='简述')
    fengge1 = models.CharField(max_length=11, verbose_name='风格1')
    fengge2 = models.CharField(max_length=11, verbose_name='风格2', null=True)
    xingji = models.CharField(max_length=3, default=5, verbose_name='星级')
    xiaoliang = models.IntegerField(default=1, verbose_name='服务量')
    guanzhu = models.IntegerField(default=11, verbose_name='关注度')

    #创建工人和评论表关系
    worker_evaluation = models.ManyToManyField(to='Comment')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name


# 需求类
class Needs(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=100)
    need = models.CharField(max_length=20, verbose_name='工长/装修公司', default='工长')
    address = models.CharField(max_length=20, verbose_name='位置')
    xiaoqu = models.CharField(max_length=20, verbose_name='小区')
    chenghu = models.CharField(max_length=20, verbose_name='称呼')
    lianxi = models.CharField(max_length=20, verbose_name='手机号')
    xuqiu = models.CharField(max_length=20, verbose_name='需求')
    huxing = models.CharField(max_length=20, verbose_name='户型')
    mianji = models.CharField(max_length=20, verbose_name='面积')
    housetype = models.CharField(max_length=20, verbose_name='状态')

#定义话题类
class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name='话题标题')
    date = models.DateField(blank=True, null=True, auto_now=True)
    image1 = models.ImageField(null=True, blank=True, upload_to='static', verbose_name='标题图像')
    text1 = models.TextField(max_length=800, blank=True, null=True)
    image2 = models.ImageField(null=True, blank=True, upload_to='static')
    text2 = models.TextField(max_length=400, blank=True, null=True)
    image3 = models.ImageField(null=True, blank=True, upload_to='static')
    text3 = models.TextField(max_length=400, blank=True, null=True)
    image4 = models.ImageField(null=True, blank=True, upload_to='static')
    text4 = models.TextField(max_length=400, blank=True, null=True)
    image5 = models.ImageField(null=True, blank=True, upload_to='static')
    text5 = models.TextField(max_length=400, blank=True, null=True)
    image6 = models.ImageField(null=True, blank=True, upload_to='static')
    text6 = models.TextField(max_length=400, blank=True, null=True)
    # 评论
    comment = models.ManyToManyField(to='Comment')
    def __unicode__(self):
        return self.title

# 定义变形记
class Change(models.Model):
    title = models.CharField(max_length=100, verbose_name='变形记标题')
    date = models.DateField(blank=True, null=True, auto_now=True)
    # 展示文件及说明
    test1 = models.TextField(max_length=500,verbose_name='变形记内容')
    img1 = models.ImageField(blank=True, null=True,verbose_name='变形记首页面')
    # 户型说明
    huxing = models.CharField(default="三室一厅", max_length=32, verbose_name='户型')
    mianji = models.IntegerField(default=110, verbose_name='面积')
    huafei = models.IntegerField(default=150000, verbose_name='花费')
    weizhi = models.CharField(default="辉煌铭苑", max_length=80, verbose_name='位置')
    # 变形记内容
    test2 = models.CharField(max_length=32,verbose_name='房屋位置')
    img2_1 = models.ImageField(blank=True, null=True,verbose_name='装修前',default="Null")
    img2_2 = models.ImageField(blank=True, null=True,verbose_name='装修后',default="Null")
    test3 = models.CharField(max_length=32,verbose_name='房屋位置_1')
    img3_1 = models.ImageField(blank=True, null=True,verbose_name='装修前_1',default="Null")
    img3_2 = models.ImageField(blank=True, null=True,verbose_name='装修后_1',default="Null")
    test4 = models.CharField(max_length=32,verbose_name='房屋位置_2')
    img4_1 = models.ImageField(blank=True, null=True,verbose_name='装修前_2',default="Null")
    img4_2 = models.ImageField(blank=True, null=True,verbose_name='装修后_2',default="Null")
    test5 = models.CharField(max_length=32,verbose_name='房屋位置_3')
    img5_1 = models.ImageField(blank=True, null=True,verbose_name='装修前_3',default="Null")
    img5_2 = models.ImageField(blank=True, null=True,verbose_name='装修后_3',default="Null")
    test6 = models.CharField(max_length=32,verbose_name='房屋位置_4')
    img6_1 = models.ImageField(blank=True, null=True,verbose_name='装修前_4',default="Null")
    img6_2 = models.ImageField(blank=True, null=True,verbose_name='装修后_4',default="Null")
    # 设计师信息
    designer = models.ForeignKey('Designer', on_delete=models.CASCADE)
    # 评论
    comment = models.ManyToManyField(to='Comment',null=True, blank=True,)
    def __unicode__(self):
        return self.title


# 评论
class Comment(models.Model):
    name = models.CharField(max_length=500, verbose_name='评论人')
    openid = models.CharField(max_length=100)
    test = models.CharField(max_length=200, verbose_name='评论内容')
    date = models.DateField(blank=True, null=True,auto_now=True, verbose_name='评论时间')
    dianzan = models.IntegerField(default=1, verbose_name='点赞')
    dianzanfunc = models.CharField(max_length=10,default='false')

    def __unicode__(self):
        return self.test
    def __str__(self):
        return self.name


#购物车表
class Shopping_Cart(models.Model):
    order_number = models.CharField(max_length=100,verbose_name='订单编号')
    openid = models.CharField(max_length=100,verbose_name='用户openid')
    days_num = models.IntegerField(default=1,verbose_name='购买天数')
    #0:待付款  1:已付款   2:待收款   3:待评价   4:售后/服务
    order_status = models.IntegerField(default=0,verbose_name='订单状态')
    add_date = models.DateField(blank=True, null=True, auto_now=True, verbose_name='下单时间')
    purchase_date = models.DateField(blank=True, null=True,verbose_name='支付时间')
    total_price = models.IntegerField(default=0,verbose_name='订单金额')
    # proper_number = models.CharField(max_length=19,default="4114231987154",verbose_name='对工账号')

    #与工人创建关系
    worker_relationship = models.ManyToManyField(to="Worker")

    #与设计师创建关系
    designer_relationship = models.ManyToManyField(to="Designer")

    def __str__(self):
        return  self.order_number





