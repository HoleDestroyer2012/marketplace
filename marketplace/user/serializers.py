from rest_framework import serializers
from .models import CustomUser, Profile
from comment.serializers import CommentSerializer

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 6},
        }


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, min_length=6)
    confirmPassword = serializers.CharField(required=True, min_length=6)

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError('Password do not match.')
        return data



class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'groups', 'user_permissions', 'profile', 'comments']
        extra_kwargs = {
            'groups': {'required': False},
            'user_permissions': {'required': False},
        }

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data