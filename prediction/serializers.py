from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    user_id = serializers.CharField(max_length=3)
    cat_id = serializers.CharField(max_length=3)
    