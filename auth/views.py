from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import permissions, serializers
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response

class MyTokenObtainPairView(TokenObtainPairView):
    permissions_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def get(requests, format=None):
        return(Response({"msg": "Get not allowed"}))

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

# from rest_framework import generics
# class RegisterView(generics.CreateAPIView):
#     querySet = User.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = RegisterSerializer