from django.contrib import admin
from api.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ User Admin """
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'tp_no']


class FoodInline(admin.StackedInline):
    """ Inline view of foods belongs to menu """
    model = Food
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """ Menu admin """
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    inlines = [FoodInline]


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    """ Food admin """
    list_display = ['id', 'name', 'menu']
    search_fields = ['id', 'name', 'menu']
    list_filter = ['menu']


class OrderedFoodInline(admin.StackedInline):
    """ Inline view of foods belongs to a order """
    model = OrderedFood
    extra = 0


class DeliveryDetailInline(admin.StackedInline):
    """ Inline view of delivery details of a order """
    model = DeliveryDetail
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Deliverers only from user model """
        if db_field.name == "deliverer":
            kwargs["queryset"] = User.objects.filter(role=User.DELIVERY)
        return super(DeliveryDetailInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Order admin """
    list_display = ['user', 'order_type']
    search_fields = ['user', 'order_type']
    list_filter = ['order_type']
    inlines = [OrderedFoodInline, DeliveryDetailInline]


@admin.register(DeliveryDetail)
class DeliveryDetail(admin.ModelAdmin):
    """ DeliveryDetail Admin """

    list_display = ['id', 'order', 'tel_no', 'current_location', 'deliverer']
    search_fields = ['id', 'user', 'tel_no', 'deliverer', 'current_location']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Deliverers only from user model """
        if db_field.name == "deliverer":
            kwargs["queryset"] = User.objects.filter(role=User.DELIVERY)
        return super(DeliveryDetail, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """ Table admin """
    list_display = ['id', 'num_of_chairs']
    search_fields = ['id', 'user']
    list_filter = ['num_of_chairs']


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    """ Table reservation admin """
    list_display = ['id', 'table', 'user', 'check_in', 'check_out']
    search_fields = ['table', 'user', 'date']