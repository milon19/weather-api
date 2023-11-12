from django.urls import path

from api.views import NextSevenDayForcastView

app_name = 'api'

urlpatterns = [
    path('forcast/', NextSevenDayForcastView.as_view(), name='forcast'),
]
