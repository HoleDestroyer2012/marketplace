from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import AdSerializer
from .models import Ad
from .filters import AdFilters


@api_view(['POST'])
def add_ad(request):

    data = request.data

    serializer = AdSerializer(data=data, many=False)

    if serializer.is_valid():
        print(request)
        # must add user!!!
        ad = Ad.objects.create(**data)
        res = AdSerializer(ad, many=False)
        return Response({'ad': res.data})
    else:
        return Response(serializer.errors)


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

@api_view(['PATCH'])
def update_ad(request, pk):

    ad = get_object_or_404(Ad, id=pk)

