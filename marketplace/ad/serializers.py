from rest_framework import serializers
from .models import AdImages, Ad
from comment.serializers import CommentSerializer


class AdImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdImages
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    images = AdImagesSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'description', 'price', 'category', 'owner', 'images', 'comments']

        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False},
            'description': {'required': True, 'allow_blank': False},
            'price': {'required': True},
        }

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data