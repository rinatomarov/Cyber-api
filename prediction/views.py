import joblib
from users.models import User
from nltk.stem import SnowballStemmer
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DataSerializer
from nltk.tokenize import word_tokenize
from posts.models import Post, Category
import nltk
import pickle
import sklearn

nltk.download('punkt')


def load():
    with open('prediction/model.pkl', 'rb') as file:
        vectorizer, clf = pickle.load(file)
    return vectorizer, clf


class PredictionView(APIView):

    def post(self, request):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data.get('title')
            # user_id = serializer.data.get('user_id')
            # cat_id = serializer.data.get('cat_id')
            vectorizer11, classifer11 = load()
            #
            vectorize_message = vectorizer11.transform([title])
            outcome = classifer11.predict(vectorize_message)[0]
            predict_proba = classifer11.predict_proba(
                vectorize_message).tolist()
            # user = User.objects.get(id=user_id)
            # cat = Category.objects.get(id=cat_id)

            # if outcome:
            #     post = Post.objects.create(
            #         title=title, author=user, category=cat)
            #     post.save()
            return Response({
                'result': outcome,
                'probability': predict_proba
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
