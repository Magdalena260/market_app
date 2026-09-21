from rest_framework import serializers
from _market_app.models import Market


class MarketSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    class Market(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(max_length=255)
        location = serializers.CharField(max_length=255)
        description =serializers.TextField()
        net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        return Market().objects.create(**validated_data)