from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    rating = models.IntegerField(default=3)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")


    def __str__(self):
        return self.product_name




class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=10, default="")
    desc = models.CharField(max_length=300)
    

    def __str__(self):
        return self.name

class Order(models.Model):
    product_id = models.IntegerField(default=0)
    product_desc = models.CharField(max_length=300, default="")

    user_id = models.IntegerField(default=0)
    ord_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=150, default="")
    address2 = models.CharField(max_length=150, default="")
    state = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=20, default="")
    

    def __str__(self):
        return self.name

class Profile(models.Model):
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=50)
    purchased_items = ArrayField(models.IntegerField(null=True,blank=True),null=True,blank=True)
    useremail = models.CharField(max_length=70, default="")

    def __str__(self):
        return self.username