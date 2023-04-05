from django.db import transaction, IntegrityError
from django.forms.models import model_to_dict
from rest_framework import serializers
from checkoutcore import models


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'


class StatusDetailSerializer(serializers.ModelSerializer):
    message = serializers.CharField(style={'input_type': 'charfield'})

    class Meta:
        model = models.Status
        fields = ['url', 'message']


class CheckoutItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.CheckoutItem
        fields = '__all__'
        read_only_fields = ['checkout']

    def get_title(self, obj):
        return obj.product.title


class CheckoutSerializer(serializers.ModelSerializer):
    items = CheckoutItemSerializer(many=True)
    total = serializers.SerializerMethodField(read_only=True)
    card_hash = serializers.CharField(write_only=True)

    class Meta:
        model = models.Checkout
        fields = '__all__'

    def get_total(self, obj):
        return obj.total

    def create(self, validated_data):
        card_hash = validated_data.pop('card_hash')
        try:
            with transaction.atomic():
                items = list(validated_data.pop('items'))
                status = models.Status.objects.filter(id='e1182812-d1b0-4585-99bf-6510497602ab')
                validated_data['status'] = status[0]
                checkout = models.Checkout.objects.create(**validated_data)
                checkout_items = []
                for item in items:
                    item['checkout'] = checkout
                    checkout_items.append(models.CheckoutItem(**item))
                checkout.items = checkout.checkout_items.bulk_create(checkout_items)
                return checkout
        except IntegrityError as e:
            raise serializers.ValidationError({"detail": e})


class CheckoutDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Checkout
        fields = '__all__'

    def get_total(self, obj):
        return obj.total

    def get_items(self, obj):
        return [{
            'title': check_item.product.title,
            'quantity': check_item.quantity,
            'price': check_item.price
        } for check_item in obj.checkout_items.all()]

    def status(self, obj):
        return model_to_dict(models.Status.objects.get(id=obj.status.id))
