from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import CustomUser
from .serializers import CreateCustomUserModelSerializer, CustomUserModelSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer

    @swagger_auto_schema(
        request_body=CreateCustomUserModelSerializer,
        responses={
            201: CreateCustomUserModelSerializer
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateCustomUserModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = self.get_serializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
