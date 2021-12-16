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

    ordered_food = FoodSerializer(many=True, read_only=True)
    order_type = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_type', 'ordered_food']

    def get_order_type(self, obj):
        return obj.get_order_type_display()


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