from django.urls import include
from django.urls import path, include
from api.api_views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('bot/', ChatBotAPIView.as_view(), name="bot"),
    path('table-reservation/', TableReservationAPIView.as_view(), name='table_reservation'),
]
