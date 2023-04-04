import core.models as models
from authcore.models import UserClient
from payment.serializers import PaymentMethodSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction, IntegrityError
from django.forms.models import model_to_dict
from config.celery import _publish


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='authcore.user.password', write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = models.Customer
        fields = ['id', 'name', 'email', 'password', 'phone']

    def create(self, validated_data):
        if models.Customer.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"detail": "User email already exists"})
        user_data = validated_data.pop('authcore')['user']
        user_data['username'] = validated_data['name']
        user_data['email'] = validated_data['email']
        user_client = UserClient.objects.create_client(**user_data)
        customer = models.Customer.objects.create(id=user_client.id, user=user_client, **validated_data)
        return customer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        self.get_token(self.user)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data


class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(write_only=True)

    class Meta:
        model = models.Address
        fields = ['id', 'customer', 'street', 'street_number', 'city', 'zipcode']
        read_only_fields = ['customer']

    def create(self, validated_data):
        user_id = validated_data.pop('customer')
        if models.Address.objects.filter(customer=user_id).exists():
            raise serializers.ValidationError({'detail': 'Address already exists'})
        customer = models.Customer.objects.get(id=user_id)
        return models.Address.objects.create(customer=customer, **validated_data)

    def update(self, instance, validated_data):
        user_id = validated_data.pop('customer')
        if not models.Customer.objects.filter(id=user_id).exists():
            raise serializers.ValidationError({"detail": "No user found"})
        instance.street = validated_data.get('street', instance.street)
        instance.street_number = validated_data.get('street_number', instance.street_number)
        instance.city = validated_data.get('city', instance.city)
        instance.zipcode = validated_data.get('zipcode', instance.zipcode)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.image.url


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
        payment_method = validated_data['payment_method']
        card_hash = validated_data.pop('card_hash')

        try:
            with transaction.atomic():
                items = list(validated_data.pop('items'))
                checkout = models.Checkout.objects.create(**validated_data)
                checkout_items = []
                for item in items:
                    item['checkout'] = checkout
                    checkout_items.append(models.CheckoutItem(**item))
                checkout.items = checkout.checkout_item.bulk_create(checkout_items)

                payload = {
                    'customer': ClientSerializer(validated_data['customer']).data['id'],
                    'payment_method': PaymentMethodSerializer(payment_method).data['name'],
                    'checkout_id': CheckoutSerializer(checkout).data['id'],
                    'card_hash': card_hash
                }

                _publish(message=payload, routing_key='payment')
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
