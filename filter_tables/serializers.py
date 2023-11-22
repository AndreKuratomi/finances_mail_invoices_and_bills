from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    receiver_name = serializers.CharField()
    receiver_email = serializers.EmailField()
