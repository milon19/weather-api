import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def get_districts_data():
    with open('api/districts.json') as f:
        data = json.load(f)
    return data


def search_location(value):
    districts = get_districts_data()
    for district in districts["districts"]:
        if 'name' in district and str(value).lower() in str(district['name']).lower():
            return district
    return None


class NextSevenDayForcastView(APIView):

    def get(self, request):
        districts = get_districts_data()

        if districts:
            districts = districts["districts"]
        else:
            return Response({"message": "failed to load districts data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lats = [dis['lat'] for dis in districts]
        longs = [dis['long'] for dis in districts]

        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lats,
            "longitude": longs,
            "hourly": "temperature_2m"
        }
        responses = openmeteo.weather_api(url, params=params)

        count = 0
        for response in responses:
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

            hourly_data = {
                "date": pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s"),
                                      end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                                      freq=pd.Timedelta(seconds=hourly.Interval()),
                                      inclusive="left"),
                "temperature_2m": hourly_temperature_2m
            }
            hourly_dataframe = pd.DataFrame(data=hourly_data)
            '''
            As API Return Date and Time in UTC. So 2PM at BDT is 08AM in UTC
            '''
            filtered_df = hourly_dataframe[hourly_dataframe['date'].dt.time == pd.to_datetime('08:00:00').time()]
            average_value = filtered_df['temperature_2m'].mean()
            districts[count]['average_temp'] = average_value
            count += 1
        sorted_data = sorted(districts, key=lambda x: x['average_temp'])[:10]
        return Response(sorted_data, status=status.HTTP_200_OK)


class ForcastForSpecificLocationView(APIView):
    def get(self, request):
        from_loc = request.query_params.get("from_loc")
        to_loc = request.query_params.get("to_loc")
        max_temp = request.query_params.get("max_temp")
        if not from_loc or not to_loc or not max_temp:
            return Response({"message": "`from_loc`, `to_loc` and `max_temp` is required"}, status=status.HTTP_404_NOT_FOUND)

        from_dist = search_location(from_loc)
        to_dist = search_location(to_loc)

        if not from_dist or not to_dist:
            return Response({"message": "location not found"}, status=status.HTTP_404_NOT_FOUND)

        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        lats = [from_dist['lat'], to_dist['lat']]
        longs = [from_dist['long'], to_dist['long']]
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lats,
            "longitude": longs,
            "hourly": "temperature_2m"
        }
        responses = openmeteo.weather_api(url, params=params)
        location = [from_dist, to_dist]
        count = 0
        for response in responses:
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

            hourly_data = {
                "date": pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s"),
                                      end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                                      freq=pd.Timedelta(seconds=hourly.Interval()),
                                      inclusive="left"),
                "temperature_2m": hourly_temperature_2m
            }
            hourly_dataframe = pd.DataFrame(data=hourly_data)
            '''
            As API Return Date and Time in UTC. So 2PM at BDT is 08AM in UTC
            '''
            filtered_df = hourly_dataframe[hourly_dataframe['date'].dt.time == pd.to_datetime('08:00:00').time()]
            average_value = filtered_df['temperature_2m'].mean()
            can_visit = True
            if average_value > float(max_temp):
                can_visit = False
            location[count]['average_temp'] = average_value
            location[count]['can_visit'] = can_visit
            count += 1
        sorted_data = sorted(location, key=lambda x: x['average_temp'])
        return Response(sorted_data, status=status.HTTP_200_OK)
