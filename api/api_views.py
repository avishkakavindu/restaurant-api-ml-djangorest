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


class ChatBotAPIView(APIView):
    """ ChatBot related operations """

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

        print('\n\n\n\n TAG: ')
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
        elif tag == 'lunch_menu':
            data, msg = self.get_foods('lunch')
        elif tag == 'dinner_menu':
            data, msg = self.get_foods('dinner')
        elif tag == 'fast_food_menu':
            data, msg = self.get_foods('fast foods')
        elif tag == 'order':
            user = User.objects.get(id=1)
            order = Order.objects.filter(user=user).latest('id')
            serializer = OrderSerializer(order)
            data = serializer.data
        elif tag == 'order_type_take_away':
            pass
        elif tag == 'order_type_deliver':
            pass
        elif tag == 'order_customization':
            pass
        elif tag == 'custom_order_detail':
            pass
        elif tag == 'order_tacking':
            pass
        elif tag == 'table_reservation':
            response = model.get_response(tag)
            data = None
        else:
            pass

        context = {
            'tag': tag,
            'probability': intent_predictions[0]['probability'],
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
                    print('\n\n\n', reservation.check_out.replace(tzinfo=None) < check_in, reservation.check_out.replace(tzinfo=None), check_in)
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
                'detail': 'Invalid time parameters',
                'data': None
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        print('\n\n\n', 'hello')
        new_reservation = None

        for table in Table.objects.filter(num_of_chairs__gte=num_of_attendees):
            is_available = self.check_availability(table, check_in, check_out)

            print('\n\n\n\n\n', is_available)

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
            "detail": detail,
            "data": data
        }

        return Response(context, status=status.HTTP_200_OK)
