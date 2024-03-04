from rest_framework import serializers
from .models import *


class AdImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdImages
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    images = AdImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'description', 'price', 'category', 'owner', 'images']

        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False},
            'description': {'required': True, 'allow_blank': False},
            'price': {'required': True},
        }