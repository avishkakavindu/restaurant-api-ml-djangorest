from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class User(AbstractUser):
    """ Custom user model """

    CUSTOMER = 0
    DELIVERY = 1

    USER_TYPES = [
        (CUSTOMER, 'Customer'),
        (DELIVERY, 'Delivery')
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    tp_no = models.CharField(max_length=12)
    role = models.PositiveSmallIntegerField(choices=USER_TYPES, default=CUSTOMER)

    def __str__(self):
        return self.username


class Menu(models.Model):
    """ Holds menu types information """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Food(models.Model):
    """ Holds food/meal information """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    menu = models.ForeignKey(Menu, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Holds order details """
    DELIVERY = 0
    TAKEAWAY = 1

    ORDER_TYPES = [
        (DELIVERY, 'Delivery'),
        (TAKEAWAY, 'Takeaway')
    ]

    order_id = models.CharField(max_length=255, unique=True)
    order_type = models.SmallIntegerField(choices=ORDER_TYPES, default=TAKEAWAY)
    message = models.TextField(null=True)
    ordered_food = models.ManyToManyField(
        Food,
        through='OrderedFood',
        through_fields=['order', 'food']
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id


class OrderedFood(models.Model):
    """ Holds foods belongs to a order """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return '{}-{}'.format(self.order.order_id, self.food)


class DeliveryDetail(models.Model):
    """ Holds delivery details """
    address = models.CharField(max_length=255)
    tel_no = models.CharField(max_length=12)
    current_location = models.CharField(max_length=255)
    deliverer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.order.order_id


class Table(models.Model):
    """ Holds table details """
    num_of_chairs = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class TableReservation(models.Model):
    """ Holds table reservation details """
    check_in = models.DateTimeField(default=datetime.now())
    check_out = models.DateTimeField(default=datetime.now())
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.table, self.user)
