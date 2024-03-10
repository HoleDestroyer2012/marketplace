from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


from .models import Comment, CommentImages
from .serializers import CommentSerializer, CommentImagesSerializer
from ad.models import Ad


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    data = request.data
    user = request.user
    print(user)
    ad = get_object_or_404(Ad, id=data['ad'])

    if ad.owner == request.user:
        raise PermissionDenied(
            'You cant add comment under your ad')

    exist_comment = Comment.objects.filter(ad=ad, user=user).exists()
    if exist_comment:
        raise PermissionDenied(
            'You already left a comment on this ad')

    data['user'] = user.id
    serializer = CommentSerializer(data=data, many=False)

    if serializer.is_valid() and ad:
        comment = serializer.save()
        res = CommentSerializer(comment, many=False)
        return Response({'comment': res.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_comment(request, comment_pk):

    comment = get_object_or_404(Comment, id=comment_pk)

    serializer = CommentSerializer(comment, many=False)

    return Response({'comment': serializer.data})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_pk):

    user = request.user

    comment = get_object_or_404(Comment, id=comment_pk)

    if user != comment.user:
        raise PermissionDenied(
            'You dont have permission to edit this comment')

    allowed_fields = {'comment_text', 'mark'}
    data_to_update = {}
    for field in allowed_fields:
        if field in request.data:
            data_to_update[field] = request.data[field]

    serializer = CommentSerializer(
        comment, data=data_to_update, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_pk):

    comment = get_object_or_404(Comment, id=comment_pk)

    if request.user != comment.user:
        raise PermissionDenied(
            'You dont have permission to delete this comment')

    comment.delete()
    return Response({'message': 'Comment deleted succesfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_images(request, comment_pk):

    files = request.FILES.getlist('images')
    comment = get_object_or_404(Comment, id=comment_pk)

    if not files:
        return Response({'error': 'No images were provided'}, status=status.HTTP_400_BAD_REQUEST)

    if request.user != comment.user:
        raise PermissionDenied(
            'You dont have permission to delete this comment')

    images = []
    for f in files:
        image = CommentImages.objects.create(comment=comment, image=f)
        images.append(image)

    serializer = CommentImagesSerializer(images, many=True)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
