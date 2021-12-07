from rest_framework.response import Response
from rest_framework.views import APIView
from api.chatbot.bot import ChatBot


class ChatBotAPIView(APIView):
    """ ChatBot related operations """

    def post(self, request, *args, **kwargs):
        pattern = request.data.get('pattern')

        model = ChatBot()

        # get intent predictions
        intent_predictions = model.get_predictions(pattern)
        tag = intent_predictions[0]['intent']

        if tag == 'greetings':
            pass
        elif tag == 'goodbye':
            pass
        elif tag == 'noanswer':
            pass
        elif tag == 'options':
            pass
        elif tag == 'menu':
            pass
        elif tag == 'breakfast_menu':
            pass
        elif tag == 'lunch_menu':
            pass
        elif tag == 'dinner_menu':
            pass
        elif tag == 'fast_food_menu':
            pass
        elif tag == 'order':
            pass
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
            pass
        elif tag == 'invalid':
            pass
        elif tag == 'name':
            pass
        elif tag == 'about':
            pass
        else:
            pass

        response = model.get_response(tag)


        context = {
            'tag': tag,
            'probability': intent_predictions[0]['probability'],
            'response': response
        }
        return Response(context)
