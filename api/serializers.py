from rest_framework import serializers
from api.models import *


class MenuSerializer(serializers.ModelSerializer):
    """ Serializer for the Menu model """

    class Meta:
        model = Menu
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    """ Serializer for the Food model """

    class Meta:
        model = Food
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for the Order model """

    ordered_foods = serializers.RelatedField(many=True, queryset=OrderedFood.objects.all())

    class Meta:
        model = Order
        fields = []


class TableSerializer(serializers.ModelSerializer):
    """ Serializer for the Table model """

    class Meta:
        model = Table
        fields = '__all__'


class TableReservationSerializer(serializers.ModelSerializer):
    """ Serializer for the TableReservation model """

    class Meta:
        model = TableReservation
        fields = '__all__'