from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DataSerializer
from nltk.tokenize import word_tokenize
from posts.models import Post, Category
import nltk
import pickle

nltk.download('punkt')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from users.models import User

from sklearn.externals import joblib


class PredictionView(APIView):
    def post(self, request):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data.get('title')
            model = pickle.load(open('prediction/model_final.pkl', 'rb'))
            pm = process_message(title)
            outcome = model.classify(pm)
            user = User.objects.get(id=1)
            cat = Category.objects.get(id=1)
            if outcome:
                post = Post.objects.create(title=title, author=user, category=cat)
                post.save()
            return Response({
                'result': outcome,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def process_message(message, lower_case=True, stem=True, stop_words=True, gram=2):
    if not lower_case:
        message = message.lower()
    words = word_tokenize(message)
    words = [w for w in words if len(w) > 2]
    if gram > 1:
        w = []
        for i in range(len(words) - gram + 1):
            w += [' '.join(words[i:i + gram])]
        return w
    if stop_words:
        sw = stopwords.words("russian")
    if stem:
        stemmer = SnowballStemmer("russian")
        words = [stemmer.stem(word) for word in words]
    print(words)
    return words