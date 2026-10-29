from rest_framework import serializers

from .models import Destinataire, ReleveTemperature, Transport


class DestinataireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinataire
        fields = "__all__"


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = "__all__"


class ReleveTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleveTemperature
        fields = "__all__"
