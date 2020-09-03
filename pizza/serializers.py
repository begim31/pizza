from rest_framework import serializers
from pizza.models import Order


class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ['updated', 'created']


class RetrieveOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'
