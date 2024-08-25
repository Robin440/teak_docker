from rest_framework import serializers
from product.models import *


class CategorySerializers(serializers.ModelSerializer):
    """Category serializer"""
    class Meta:
        """meta class"""
        model = Category
        # fields = "__all__"
        exclude = ['uuid']


class SubCategorySerializers(serializers.ModelSerializer):
    """Sub category serializer"""
    category = CategorySerializers(read_only = True)
    class Meta:
        """meta class"""
        model = Subcategory
        fields = "__all__"
        exclude = ['uuid']
        

class SubofSubSerializers(serializers.ModelSerializer):
    """Sub of sub category serializer"""
    sub_category = SubCategorySerializers(read_only = True)
    class Meta:
        """meta class"""
        model = SubofSub
        fields = "__all__"
        exclude = ['uuid']

class ProductSerializer(serializers.ModelSerializer):
    """Product serializer"""
    category = CategorySerializers(read_only = True)
    class Meta:
        """meta class"""
        model = Product
        fields = "__all__"
        exclude = ['uuid']

        