from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import status
from django.http import JsonResponse
import json
from django.contrib import messages
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer


class Cat(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            alias = serializer.data.get('alias')
            cat = Category.objects.create(name=name, alias=alias)
            cat.save()
            return Response({
                'success': 'Добавлена новая категория',

            }, status=status.HTTP_200_OK)


    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



class Post_view(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)