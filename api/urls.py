from django.urls import path

from api.views import NextSevenDayForcastView, ForcastForSpecificLocationView

app_name = 'api'

urlpatterns = [
    path('forcast/', NextSevenDayForcastView.as_view(), name='forcast'),
    path('forcast-specific-loc/', ForcastForSpecificLocationView.as_view(), name='forcast_specific_loc'),
]
