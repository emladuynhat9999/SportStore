from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=250)
    name_no_bind = models.SlugField(max_length=250, null=True)
    price = models.FloatField(default=0.0)
    price_origin = models.FloatField(null=True)
    image = models.ImageField(upload_to="store/images",
                              default="store/images/default.png")
    content = RichTextUploadingField(blank=True, null=True)
    short_content = RichTextUploadingField(blank=True, null=True)
    public_day = models.DateTimeField(default=datetime.datetime.now)
    viewed = models.IntegerField(default=0)
    meterial = models.CharField(max_length=250)
    where_production = models.CharField(max_length=250)
    remains_quanity = models.IntegerField(default=0)
    # name -> name url (áo thun -> ao-thun)
    
   
    def __str__(self):
        return self.name

# Class Brand relate Product
class Brand(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# Class Discount_product relate Product: 
class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    discount = models.FloatField(default=0)

    def __str__(self):
        return self.discount


# Class Customer
class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=False)
    fullname = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=500, unique=False)

    def __str__(self):
        return self.username

# Class Client
class Client(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=250, unique=False)

    def __str__(self):
        return self.username

class UserProfileInfo(models.Model):
    # Create relationship from this class to User
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    # Add any more attribute you want    
    address = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "store/images/", default="store/images/people_default.png")    
    
    def __str__(self):
        return self.user.username 

class Contact(models.Model):
    fullname = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=250,)
    content = models.CharField(max_length=500,)

    def __str__(self):
        return self.fullname