from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AdSerializer

from .models import Ad


@api_view(['POST'])
def add_ad(request):

    data = request.data

    serializer = AdSerializer(data=data, many=False)

    if serializer.is_valid():
        # must add user!!!
        ad = Ad.objects.create(**data)
        res = AdSerializer(ad, many=False)
        return Response({'ad': res.data})
    else:
        return Response(serializer.errors)
