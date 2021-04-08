from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)