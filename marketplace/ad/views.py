from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from .serializers import AdSerializer, AdImagesSerializer
from .models import Ad, AdImages
from .filters import AdFilters


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_ad(request):

    data = request.data

    serializer = AdSerializer(data=data, many=False)

    if serializer.is_valid():
        print(request)
        ad = Ad.objects.create(**data, owner=request.user)
        res = AdSerializer(ad, many=False)
        return Response({'ad': res.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_ad(request, pk):

    ad = get_object_or_404(Ad, id=pk)

    serializer = AdSerializer(ad, many=False)

    return Response({'ad': serializer.data})


@api_view(['GET'])
def get_all_ads(request):

    filterset = AdFilters(request.GET, queryset=Ad.objects.all().order_by('id'))

    count = filterset.qs.count()

    # Pagination
    resPerPage = 3

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = AdSerializer(queryset, many=True)

    return Response({
        'count': count,
        'resPerPage': resPerPage,
        'ads': serializer.data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_ad_images(request):
    print(request.data)
    data = request.data
    files = request.FILES.getlist('images')

    if 'ad' not in data:
        return Response({'error': 'Missing or invaild field "ad" in data'}, status=status.HTTP_400_BAD_REQUEST)

    ad = get_object_or_404(Ad, id=data['ad'])

    if ad.owner != request.user:
        return Response({'error': 'You are not allowded to upload images to this add'}, status=status.HTTP_403_FORBIDDEN)

    images = []

    for f in files:
        image = AdImages.objects.create(ad=ad, image=f)
        images.append(image)

    serializer = AdImagesSerializer(images, many=True)

    return  Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_ad(request, pk):

    data = request.data
    ad = get_object_or_404(Ad, id=pk)

    #Check if user the same
    if ad.owner != request.user:
        return Response({'error': 'You can not update this ad'}, status=status.HTTP_403_FORBIDDEN)

    serializer = AdSerializer(ad, data=data, partial=True, many=False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ad(request, pk):
    
    ad = get_object_or_404(Ad, id=pk)

    #Check if user is owner of this ad
    if request.user != ad.owner:
        return Response({'error': 'You can not delete this ad'}, status=status.HTTP_403_FORBIDDEN)

    args = {'ad': pk}
    images = AdImages.objects.filter(**args)
    for i in images:
        i.delete()

    ad.delete()

    return Response({'detail': 'Ad was succesfully deleted'}, status=status.HTTP_200_OK)