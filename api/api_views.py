from datetime import datetime
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from api.chatbot.bot import ChatBot
from api.models import *
from api.serializers import *
from rest_framework import mixins, generics, status
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework import authentication, permissions
from django.db.models import Q
from rest_framework import generics


class ChatBotAPIView(APIView):
    """ ChatBot related operations """

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_menu(self, menu):
        """ returns a menu object """
        return Menu.objects.get(name=menu)

    def get_foods(self, menu):
        foods = Food.objects.filter(menu=self.get_menu(menu))
        serializer = FoodSerializer(foods, many=True)
        data = serializer.data
        msg = "Here are the foods..."

        return data, msg

    def post(self, request, *args, **kwargs):
        pattern = request.data.get('pattern')

        model = ChatBot()

        # get intent predictions
        intent_predictions = model.get_predictions(pattern)
        tag = intent_predictions[0]['intent']

        # print('\n\n\n\n TAG: ')
        response = data = ''

        if tag == 'greetings':
            response = model.get_response(tag)
        elif tag == 'goodbye':
            response = model.get_response(tag)
        elif tag == 'noanswer':
            response = model.get_response(tag)
        elif tag == 'options':
            response = model.get_response(tag)
        elif tag == 'invalid':
            response = model.get_response(tag)
        elif tag == 'name':
            response = model.get_response(tag)
        elif tag == 'about':
            response = model.get_response(tag)
        elif tag == 'menu':
            menu = Menu.objects.all()
            serializer = MenuSerializer(menu, many=True)
            data = serializer.data
            response = "Please select a menu"
        elif tag == 'breakfast_menu':
            data, msg = self.get_foods('breakfast')
            response = "Please, select a dish"
        elif tag == 'lunch_menu':
            data, msg = self.get_foods('lunch')
            response = "Please, select a dish"
        elif tag == 'dinner_menu':
            data, msg = self.get_foods('dinner')
            response = "Please, select a dish"
        elif tag == 'fast_food_menu':
            data, msg = self.get_foods('fast foods')
            response = "Please, select a dish"
        elif tag == 'order':
            user = User.objects.get(id=request.user.id)
            try:
                order = Order.objects.filter(user=user).latest('id')
            except Order.DoesNotExist:
                context = {
                    'tag': tag,
                    # 'probability': intent_predictions[0]['probability'],
                    'response': 'No order found!',
                    'data': None
                }
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order)
            data = serializer.data
            response = "Here's your order details"
        elif tag == 'order_type_take_away':
            user = User.objects.get(id=request.user.id)
            order = Order.objects.filter(user=user).latest('id')
            order.order_type = Order.TAKEAWAY
            order.save()
            serializer = OrderSerializer(order)
            data = serializer.data
            response = "Order type changed to Take Away"
        elif tag == 'order_type_deliver':
            user = User.objects.get(id=request.user.id)
            order = Order.objects.filter(user=user).latest('id')
            order.order_type = Order.DELIVERY
            order.save()
            serializer = OrderSerializer(order)
            data = serializer.data
            response = "Order type changed to Delivery"
        elif tag == 'order_customization':
            response = 'Ordered dishes.'
            user = User.objects.get(id=request.user.id)
            try:
                order = Order.objects.filter(user=user, is_active=True).latest('id')
                serializer = OrderSerializer(order)
                data = serializer.data
            except Order.DoesNotExist:
                response = "Sorry, no record found for the relevant order id please check whether the id is correct"
                data = None
        elif tag == 'order_history':
            user = User.objects.get(id=request.user.id)

            order = Order.objects.filter(user=user)
            if not order.exists():
                response = "Sorry, no previous orders!"

            serializer = OrderSerializer(order, many=True)
            data = serializer.data

        elif tag == 'custom_order_detail':
            pass
        elif tag == 'table_reservation':
            response = model.get_response(tag)
            data = None
        else:
            pass

        context = {
            'tag': tag,
            # 'probability': intent_predictions[0]['probability'],
            'response': response,
            'data': data
        }
        return Response(context, status=status.HTTP_200_OK)


class TableReservationAPIView(APIView):
    """ Table Reservation APIView """

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def check_availability(self, table, check_in, check_out):
        available_tables = []

        # if no reservations fo the table
        if TableReservation.objects.filter(table=table).exists():
            reservations = TableReservation.objects.filter(table=table)

            for reservation in reservations:
                if reservation.check_in.replace(tzinfo=None) > check_out or reservation.check_out.replace(tzinfo=None) < check_in:
                    # print('\n\n\n', reservation.check_out.replace(tzinfo=None) < check_in, reservation.check_out.replace(tzinfo=None), check_in)
                    available_tables.append(True)
                else:
                    available_tables.append(False)
            return all(available_tables)
        return True

    def post(self, request, *args, **kwargs):
        check_in = request.data.get('check_in')
        check_in = datetime.strptime(check_in, '%b %d %Y %I:%M%p')
        check_out = request.data.get('check_out')
        check_out = datetime.strptime(check_out, '%b %d %Y %I:%M%p')
        num_of_attendees = request.data.get('num_of_attendees')

        if check_in > check_out:
            context = {
                "tag": 'reservation_status',
                'response': 'Invalid time parameters',
                'data': None
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        new_reservation = None

        for table in Table.objects.filter(num_of_chairs__gte=num_of_attendees):
            is_available = self.check_availability(table, check_in, check_out)

            if is_available:
                new_reservation = TableReservation.objects.create(
                    check_in=check_in,
                    check_out=check_out,
                    table=table,
                    user=User.objects.get(id=request.user.id)
                )
                break

        if new_reservation is not None:
            serializer = TableReservationSerializer(new_reservation)
            data = serializer.data
            detail = "Your Reservation Details"
        else:
            detail = "Sorry! No tables available at the moment."
            data = None

        context = {
            "tag": 'reservation_status',
            "response": detail,
            "data": data
        }

        return Response(context, status=status.HTTP_200_OK)


class OrderCreateUpdateAPIView(APIView):
    """ Ordering APIView """

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        food = Food.objects.get(id=request.data.get('food_id'))
        quantity = request.data.get('quantity')

        try:
            order = Order.objects.get(user=user, is_active=True)
        except Order.DoesNotExist:
            order = Order.objects.create(user=user)

        ordered_food, created = OrderedFood.objects.update_or_create(order=order, food=food, quantity=quantity)
        order.ordered_food.add(food)

        serializer = OrderSerializer(order)

        context = {

            'response': 'Dish added to your order.',
            'data': serializer.data
        }

        return Response(context)


class OrderCustomizationAPIView(APIView):
    """ Order customization APIView """

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    CUSTOMIZATIONS = dict(Customization.CUSTOMIZATIONS)

    def get(self, request, *args, **kwargs):
        ordered_food = self.kwargs.get('pk')
        user = request.user.id
        order = Order.objects.filter(user=user).latest('id')
        # ordered food object
        o_f_obj_id = OrderedFood.objects.get(order=order, food=Food.objects.get(id=ordered_food)).id
        print('\n\n\n food:', o_f_obj_id)

        customizations = OrderCustomization.objects.filter(ordered_food=o_f_obj_id)
        serializer = OrderCustomizationSerializer(customizations, many=True)

        possible_customizations = Customization.objects.filter(food=OrderedFood.objects.get(id=o_f_obj_id).food).values_list('customization')

        possible_customizations = [self.CUSTOMIZATIONS[cus[0]] for cus in possible_customizations]

        context = {
            'tag': 'customization_history',
            'response': 'Your current customizations.',
            'data': {
                "ordered_customized_foods": serializer.data,
                'possible_customizations': possible_customizations
            }
        }

        return Response(context, status=status.HTTP_200_OK)

    def get_key_by_value(self, value, customizations=CUSTOMIZATIONS):
        return list(customizations.keys())[list(customizations.values()).index(value)]

    def get_object(self, id):
        return OrderedFood.objects.get(id=id)

    def post(self, request, *args, **kwargs):
        ordered_food_id = self.kwargs.get('pk')
        customization = request.data.get('customization')

        user = request.user.id
        order = Order.objects.filter(user=user).latest('id')
        # ordered food object
        o_f_obj_id = OrderedFood.objects.get(order=order, food=Food.objects.get(id=ordered_food_id)).id

        food = OrderedFood.objects.get(id=o_f_obj_id).food

        customization = Customization.objects.get(customization=self.get_key_by_value(customization), food=food)
        order_customization, created = OrderCustomization.objects.update_or_create(ordered_food=self.get_object(o_f_obj_id), customization=customization)
        serializer = OrderCustomizationSerializer(order_customization)

        context = {
            'data': serializer.data
        }
        
        return Response(context)


class TrainAPIView(APIView):
    """ Chat bot training APIView """

    def get(self, request, *args, **kwargs):
        model = ChatBot()
        model.train()

        return Response({'detail': 'Model Trained!'})


class OrderHistoryAPIView(APIView):
    """ Order history(week worth of) APIView """

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        queryset = Order.objects.filter(user=user)

        serializer = OrderSerializer(queryset, many=True)

        context = {
            'data': serializer.data
        }

        return Response(context, status=status.HTTP_200_OK)

