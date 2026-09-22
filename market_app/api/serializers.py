from rest_framework import serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model: Market
        exclude = []

def validate_no_x(value):
    errors = []

    if 'X' in value:
        errors.append('no X in location')

    if 'Y' in value:
        errors.append('no Y in location')

    if errors:
        raise serializers.ValidationError(errors)

    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(
        max_length=255,
        validators=[validate_no_x]
    )
    description = serializers.CharField()
    net_worth = serializers.DecimalField(
        max_digits=100,
        decimal_places=2
    )

    def create(self, validated_data):
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get(
            'location',
            instance.location
        )
        instance.description = validated_data.get(
            'description',
            instance.description
        )
        instance.net_worth = validated_data.get(
            'net_worth',
            instance.net_worth
        )
        instance.save()
        return instance

    def validate_location(self, value):
        if 'X' in value:
            raise serializers.ValidationError('no X in location')
        return value

    class MarketSerrializer(serializers.ModelSerializer):
       class Meta:
        model = Market
       fields = '__all__'

       def validate_name(self,value):
        errors = []

        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
            errors.append('no Y in location')

            if errors:
                raise serializers.ValidationError(errors)

            return value

class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    #markets = MarketSerializer(many=True, read_only=True)
    markets = serializers.StringRelatedField(many=True)
    

class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) !=len(value):
            raise serializers.ValidationError({"message": "passt nicht min ids"})
        return value


    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets)
        return seller


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all()
    )
    seller = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all()
    )

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description',
            instance.description
        )
        instance.price = validated_data.get('price', instance.price)
        instance.market = validated_data.get('market', instance.market)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.save()
        return instance