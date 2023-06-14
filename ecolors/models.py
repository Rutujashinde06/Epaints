from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Paints(models.Model):
    CAT=((1,'Oil-Based'),(2,'Water-Based'))
    name=models.CharField(max_length=50,verbose_name="Color Shade")
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    price=models.FloatField()
    status=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to="image")

    def __str__(self):
        return self.name


class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Paints,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)    


class Order(models.Model):
    order_id=models.IntegerField()
    pid=models.ForeignKey(Paints,on_delete=models.CASCADE,db_column='pid')
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    qty=models.IntegerField()

class OrderHistory(models.Model):
    order_id=models.CharField(max_length=450,verbose_name="Order Id")
    pay_id=models.CharField(max_length=450,verbose_name="Pay Id")
    sign=models.CharField(max_length=400,verbose_name="Signature")
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')

    def __str__(self):
        return self.order_id
    
