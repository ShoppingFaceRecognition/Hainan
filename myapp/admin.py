from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'tel', 'gender', 'age', 'view_difficult', 'Consumption_frequency',
                    'face_img_path', 'fen']

    fieldsets = [
        ('用户', {'fields': ['username']}),
        ('密码', {'fields': ['password']}),
        ('电话', {'fields': ['tel']}),
        ('性别/年龄', {'fields': ['gender', 'age']}),
        ('视障', {'fields': ['view_difficult']}),
        ('照片', {'fields': ['face_img_path']}),
        ('消费次数/积分', {'fields': ['Consumption_frequency', 'fen']}),
    ]


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'price', 'is_activity', 'introduce', 'img']

    fieldsets = [('商品名', {'fields': ['name']}),
                 ('商品数量', {'fields': ['number']}),
                 ('商品价格', {'fields': ['price']}),
                 ('是否活动中', {'fields': ['is_activity']}),
                 ('商品简介', {'fields': ['introduce']}),
                 ('图片', {'fields': ['img']}),
                 ]

@admin.register(jf_Commodity)
class jf_CommodityAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'price', 'introduce', 'img']

    fieldsets = [('商品名', {'fields': ['name']}),
                 ('商品数量', {'fields': ['number']}),
                 ('商品所需积分', {'fields': ['price']}),
                 ('商品简介', {'fields': ['introduce']}),
                 ('图片', {'fields': ['img']}),
                 ]