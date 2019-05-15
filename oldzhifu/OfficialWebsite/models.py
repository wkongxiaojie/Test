from django.db import models

# 需求表
class DemandTable(models.Model):
    name = models.CharField(max_length=20,verbose_name='姓名')
    phone = models.CharField(max_length=20,verbose_name='手机号')
    address = models.CharField(max_length=100,verbose_name='地址')
    style = models.CharField(max_length=20,verbose_name='装修风格')
    noodlesproduct = models.CharField(max_length=5,verbose_name='房屋面积')
    demandtype = models.CharField(max_length=5,verbose_name='找谁装修')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.phone


#产品中心
class ProductCenter(models.Model):
    name = models.CharField(max_length=50, verbose_name='产品名称')
    path = models.CharField(max_length=100, verbose_name='图片路径')
    path1 = models.CharField(max_length=100, verbose_name='图片路径_1')
    path2 = models.CharField(max_length=100, verbose_name='图片路径_2')
    specifications = models.CharField(max_length=20,verbose_name='规格')
    price = models.CharField(max_length=20,verbose_name='价钱')
    discount = models.CharField(max_length=20,verbose_name='打折后')
    sketch = models.CharField(max_length=50,verbose_name='简述')
    briefintroduction = models.TextField(max_length=100,verbose_name='简介')
    def __str__(self):
        return  self.name


#产品类型
class ProductType(models.Model):
    name = models.CharField(max_length=10, verbose_name='类型名称')
    path = models.CharField(max_length=100,verbose_name='图片路径')
    #于产品中心创建关系
    product_relationship = models.ManyToManyField(to='ProductCenter')
    def __str__(self):
        return  self.name




#公司信息表
class CompanyInformation(models.Model):
    name = models.CharField(max_length=50, verbose_name='产品名称')
    path = models.CharField(max_length=100, verbose_name='图片路径')
    link = models.CharField(max_length=100, verbose_name='链接路径')
    content = models.CharField(max_length=50, verbose_name='介绍')
    content1 = models.CharField(max_length=50, verbose_name='介绍_1')
    def __str__(self):
        return  self.name



#变形记表
class Metamorphosis(models.Model):
    title = models.CharField(max_length=200,verbose_name='标题')
    titleImg = models.ImageField(blank=True,null=True,verbose_name='首页图片',default="Null")
    titleTest = models.TextField(max_length=400,blank=True, null=True,default="Null", verbose_name='内容头部')
    date = models.DateField(null=True,verbose_name='创建日期')
    titleImg1 = models.ImageField(blank=True, null=True, default="Null",verbose_name='图片_1')
    titleTest1 = models.TextField(max_length=400, blank=True, null=True,default="Null",verbose_name='内容_1')

    titleImg2 = models.ImageField(blank=True, null=True,default="Null",verbose_name='图片_2')
    titleTest2 = models.TextField(max_length=400, blank=True,null=True,default="Null",verbose_name='内容_2')

    titleImg3 = models.ImageField(blank=True,null=True,default="Null",verbose_name='图片_3')
    titleTest3 = models.TextField(max_length=400,blank=True,null=True,default="Null",verbose_name='内容_3')

    def __str__(self):
        return  self.title



#留言表
class Guestbook(models.Model):
    date = models.DateField(blank=True, null=True, auto_now=True, verbose_name='评论时间')
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=50, verbose_name='电话')
    content = models.CharField(max_length=100, verbose_name='内容')

    def __str__(self):
        return  self.name


