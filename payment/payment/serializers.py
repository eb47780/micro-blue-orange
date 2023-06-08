from payment.models import StripeGateway, PaymentMethod
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class StripeGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeGateway
        fields = ['id', 'secret_key']


class PaymentGatewaySerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        StripeGateway: StripeGatewaySerializer
    }
