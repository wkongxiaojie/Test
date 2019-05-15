from django.contrib import admin
from zhifu.models import *
from OfficialWebsite.models import *
# Register your models here.
class UserConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'openid']
    list_display_links = ['name']
# 用户需求管理
class NeedsConfig(admin.ModelAdmin):
    list_display = ['chenghu', 'lianxi', 'xiaoqu', 'need', 'huxing', 'housetype']
    list_filter = ['need', 'housetype']
    search_fields = ['chenghu']

# 客户管理
class ClientConfig(admin.ModelAdmin):
    list_display = ['name', 'sex', 'age', 'huxing', 'mianji', 'phone']
    list_filter = ['sex']
    search_fields = ['name']

# 设计师管理
class DesignerConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'sex', 'age', 'exp', 'baojia', 'shenfenid','phone', 'diqu', 'xingji', 'xiaoliang']
    list_filter = ['sex', 'diqu', 'xingji']
    list_display_links = ['name']
    search_fields = ['name']
# 工人管理
class WorkerConfig(admin.ModelAdmin):
    list_display = ['id', 'sex', 'name','age', 'exp', 'baojia', 'shenfenid','phone', 'diqu']
    list_filter = ['sex', 'diqu']
    search_fields = ['name']
# 话题管理
class TopicConfig(admin.ModelAdmin):
    list_display = ['id', 'title', 'date']
    def preview(self,obj):
        return '<img src="/static/static/%s" height="64" width="64" />' %(obj.photo)
# 变形计管理
class ChangeConfig(admin.ModelAdmin):
    list_display = ['id', 'title', 'designer', 'date']
    list_display_links = ['title']
# 评论管理
class CommentConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'dianzan', 'test', 'date']
    list_display_links = ['name', 'test']

#订单管理
class ShoppingCartConfig(admin.ModelAdmin):
    list_display = ['id', 'order_number', 'openid', 'days_num', 'order_status','add_date','purchase_date']
    list_display_links = ['openid']

# 用户（登录小程序的）
admin.site.register(User, UserConfig)
# 设计师
admin.site.register(Designer, DesignerConfig)
# 工人
admin.site.register(Worker, WorkerConfig)
# 客户
admin.site.register(Client, ClientConfig)
# 需求
admin.site.register(Needs, NeedsConfig)
# 话题
admin.site.register(Topic, TopicConfig)
# 变形记
admin.site.register(Change, ChangeConfig)
# 评论
admin.site.register(Comment, CommentConfig)
#订单
admin.site.register(Shopping_Cart, ShoppingCartConfig)

############################################################################################################################################################

#需求管理
class DemandConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address','style','noodlesproduct','demandtype']
    list_display_links = ['name']



#产品中心管理
class ProductCenterConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'path', 'specifications', 'price', 'discount']
    list_display_links = ['name']
    search_fields = ['name','specifications']


#产品类型管理
class ProductTypeConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'path']
    list_display_links = ['name']
    search_fields = ['name']

#公司管理
class CompanyInformationConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'path']
    list_display_links = ['name']
    search_fields = ['name']

#变形记管理
class MetamorphosisConfig(admin.ModelAdmin):
    list_display = ['id','title','date']
    list_display_links = ['title']
    search_fields = ['title']

#留言管理
class GuestbookConfig(admin.ModelAdmin):
    list_display = ['date', 'name', 'phone','content']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(DemandTable, DemandConfig)
admin.site.register(ProductCenter, ProductCenterConfig)
admin.site.register(ProductType, ProductTypeConfig)
admin.site.register(CompanyInformation, CompanyInformationConfig)
admin.site.register(Metamorphosis,MetamorphosisConfig)
admin.site.register(Guestbook,GuestbookConfig)



