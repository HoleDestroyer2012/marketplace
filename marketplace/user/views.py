from datetime import timedelta, datetime

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from .models import CustomUser, UserRoles
from .serializers import SignUpSerializer, CustomUserSerializer, ResetPasswordSerializer
from utils.helpers import get_current_host
from .permissions import IsModer, NotBanned


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not CustomUser.objects.filter(email=data['email']).exists():

            user = CustomUser.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
                password=make_password(data['password'])
            )

            return Response({'detail': 'User succesfully registred'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'detail': 'User already exist'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):

    user = CustomUserSerializer(request.user)

    return Response(user.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):

    user = request.user
    data = request.data

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    serializer = CustomUserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):

    data = request.data

    user = get_object_or_404(CustomUser, email=data['email'])

    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)

    user.user_profile.reset_password_token = token
    user.user_profile.reset_password_expire = expire_date

    user.user_profile.save()

    host = get_current_host(request)

    link = f'{host}api/reset_password/{token}/'
    body = f'Your password reset link is: {link}'

    send_mail(
        'Password reset link',
        body,
        'noreply@email.ru',
        [data['email']]
    )

    return Response({'details': 'Password reset email sent to: {email}'.format(email=data['email'])})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token):

    data = request.data

    user = get_object_or_404(
        CustomUser, user_profile__reset_password_token=token)

    if user.user_profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token in expired'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ResetPasswordSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    user.password = make_password(serializer.data['password'])

    user.user_profile.reset_password_token = ''
    user.user_profile.reset_password_expire = None

    user.user_profile.save()
    user.save()

    return Response({'detail': 'Password reset succesfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsModer, NotBanned])
def ban_user(request, user_id):

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == UserRoles.MODERATOR or user.is_superuser == True:
        raise PermissionDenied('You cant ban other Moders or Admin')

    user.is_banned = True
    user.save()

    return Response({'detail': 'User was succesfully banned'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsModer, NotBanned])
def unban_user(request, user_id):

    user = get_object_or_404(CustomUser, id=user_id)

    if user.is_banned == False:
        return Response({'error': 'This user is not banned'}, status=status.HTTP_400_BAD_REQUEST)

    user.is_banned = False
    user.save()

    return Response({'detail': 'User was succesfully unbanned'}, status=status.HTTP_200_OK)
