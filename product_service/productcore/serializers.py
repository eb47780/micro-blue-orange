from rest_framework import serializers
from productcore import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.image.url
