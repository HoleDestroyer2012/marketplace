from rest_framework import serializers

from .models import Comment, CommentImages

class CommentImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentImages
        fields = ('id', 'image')


class CommentSerializer(serializers.ModelSerializer):
    images = CommentImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'comment_text', 'mark', 'user', 'ad', 'images')

        extra_kwargs = {
            'comment_text': {'required': True},
            'ad': {'required': True},
            'mark': {'min_value': 1, 'max_value': 5}
        }