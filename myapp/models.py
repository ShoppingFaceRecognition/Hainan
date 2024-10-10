
from django.db import models
from django.contrib.auth.models import User
import os.path
from django.db import models
from django.contrib.auth.models import User

from PIL import Image
from django.db.models.fields.files import ImageFieldFile

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=150)
    password =models.CharField(max_length=150)
    tel = models.IntegerField()
    gender = models.BooleanField()
    age = models.IntegerField()
    view_difficult = models.BooleanField()
    Consumption_frequency = models.IntegerField()
    face_img_path = models.ImageField(upload_to='images/user/',null=True,blank=True)
    fen=models.IntegerField()


class Commodity(models.Model):
    name = models.CharField(max_length=255)
    introduce=models.CharField(max_length=255)
    number = models.IntegerField()
    price = models.FloatField()
    is_activity = models.BooleanField()
    img = models.ImageField(upload_to='images/commodity',null=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class jf_Commodity(models.Model):
    name = models.CharField(max_length=255)
    introduce=models.CharField(max_length=255)
    number = models.IntegerField()
    price = models.FloatField()
    # is_activity = models.BooleanField()
    img = models.ImageField(upload_to='images/commodity',null=True)

class ExchangeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(jf_Commodity, on_delete=models.CASCADE)
    exchange_date = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)