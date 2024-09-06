from django.db import models
import uuid

class Unit(models.Model):
    """Unit model"""
    uuid = models.UUIDField(primary_key= True,default= uuid.uuid4)
    name = models.CharField(max_length=500, null= True,blank = True)
    description = models.TextField(null=True, blank = True)

    def __str__(self):
        return self.name if self.name else "Unnamed"
    

class Category(models.Model):
    """Category model"""
    uuid = models.UUIDField(primary_key= True,default= uuid.uuid4)
    name = models.CharField(max_length=500, null= True,blank = True)

    description = models.TextField(null=True, blank = True)
    image = models.ImageField(upload_to='category_images',null = True, blank = True)
    def __str__(self):
        return self.name if self.name else "Unnamed"

class Subcategory(models.Model):
    """subcategory model"""
    uuid = models.UUIDField(primary_key= True,default= uuid.uuid4)
    name = models.CharField(max_length=500, null= True,blank = True)

    description = models.TextField(null=True, blank = True)
    image = models.ImageField(upload_to='category_images',null = True, blank = True)
    # category = models.ForeignKey(Category,on_delete=models.SET_NULL,null = True, blank = True)

    def __str__(self):
        return self.name if self.name else "Unnamed"

class SubofSub(models.Model):
    """sub-subcategory model"""
    uuid = models.UUIDField(primary_key= True,default= uuid.uuid4)
    name = models.CharField(max_length=500, null= True,blank = True)

    description = models.TextField(null=True, blank = True)
    image = models.ImageField(upload_to='category_images',null = True, blank = True)
    # sub_category = models.ForeignKey(Subcategory,on_delete=models.SET_NULL,null = True, blank = True)

    def __str__(self):
        return self.name if self.name else "Unnamed"

class Product(models.Model):
    """product model"""
    uuid = models.UUIDField(primary_key= True,default= uuid.uuid4,editable=False)
    name = models.CharField(max_length=500, null= True,blank = True)

    description = models.TextField(null=True, blank = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL,null= True , blank= True)
    qty = models.IntegerField(default=0)

    #image fields
    image_one = models.ImageField(upload_to='product_images',null = True, blank = True)
    image_two = models.ImageField(upload_to='product_images',null = True, blank = True)
    image_three = models.ImageField(upload_to='product_images',null = True, blank = True)
    image_four = models.ImageField(upload_to='product_images',null = True, blank = True)
    image_five = models.ImageField(upload_to='product_images',null = True, blank = True)

    status = models.BooleanField(default=True)

    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null = True, blank = True)
    sub_category = models.ForeignKey(Subcategory,on_delete=models.SET_NULL,null = True, blank = True)
    sub_of_sub = models.ForeignKey(SubofSub,on_delete=models.SET_NULL,null = True, blank = True)

    sold_by = models.CharField(max_length=100,default="Teak Wood Factory")
    material = models.CharField(max_length=100,default="Teak")

    brand = models.CharField(max_length=100,default="TeakWood")
    color  = models.CharField(max_length=100,default="Brown")

    size = models.CharField(max_length=100,null = True, blank = True)
    warranty = models.IntegerField(default= 2)

    number_of_box = models.IntegerField(null = True, blank = True)
    features = models.CharField(max_length=100,default="100 % Teakwood")

    country_of_origin = models.CharField(max_length=100,default="Made in India")
    video = models.FileField(upload_to='product_videos', null=True, blank=True)

    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name if self.name else "Unnamed"

    class Meta:
        """adding verbose name"""
        verbose_name = "Product"  # Singular verbose name
        verbose_name_plural = "Products"  # Plural verbose name




# backend developed by robin rajan

# mob : 8086712029I 