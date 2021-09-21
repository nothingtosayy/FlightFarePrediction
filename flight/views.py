import pandas as pd
from django.shortcuts import render
import pickle
import numpy as np

import sklearn
# Create your views here.

def home(request):
    return render(request, 'home.html')

def predict_Price(source, destination, airline, total_stops, journey_day, journey_month, dep_hour, dep_min,
                  arr_hour, arr_min, dur_hour, dur_min):
    model = pickle.load(open("my_csvfiles/flight_fare_prediction.sav", "rb"))
    scaled = pickle.load(open("my_csvfiles/columns_flight_fare_prediction.sav", "rb"))
    loc_indices = []
    print(scaled)
    loc_indices.append(scaled.index(source.lower()))
    loc_indices.append(scaled.index(destination.lower()))
    loc_indices.append(scaled.index(airline.lower()))
    x = np.zeros(len(scaled))
    x[0] = total_stops
    x[1] = journey_day
    x[2] = journey_month
    x[3] = dep_hour
    x[4] = dep_min
    x[5] = arr_hour
    x[6] = arr_min
    x[7] = dur_hour
    x[8] = dur_min
    for i in loc_indices:
        if i > 0:
            x[i] = 1
    return "Predicted Price is " + str(round(model.predict([x])[0], 2)) + " " + " Ruppees"


def result(request):
    if request.method == 'POST':
        source = request.POST['source']
        destination = request.POST['destination']
        stops = request.POST['stops']
        depdate = request.POST['depdate']
        journey_day = int(pd.to_datetime(depdate, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(depdate, format="%Y-%m-%dT%H:%M").month)
        dep_hour = int(pd.to_datetime(depdate, format="%Y-%m-%dT%H:%M").hour)
        dep_minute = int(pd.to_datetime(depdate, format="%Y-%m-%dT%H:%M").minute)
        arrdate = request.POST['arrdate']
        arr_day = int(pd.to_datetime(arrdate, format="%Y-%m-%dT%H:%M").day)
        arr_hour = int(pd.to_datetime(arrdate, format="%Y-%m-%dT%H:%M").hour)
        arr_minute = int(pd.to_datetime(arrdate, format="%Y-%m-%dT%H:%M").minute)
        airline = request.POST['airline']
        if journey_day == arr_day:
            dur_hour = dep_hour - arr_hour
            dur_minute = dep_minute - arr_minute
            if (dur_hour < 0) and (dur_minute > 0):
                dur_hour = -(dur_hour)
                dur_minute = dur_minute
            elif (dur_minute < 0) and (dur_hour > 0):
                dur_minute = -(dur_minute)
                dur_hour = dur_hour
            else:
                dur_hour = -(dur_hour)
                dur_minute = -(dur_minute)
        else:
            if (dep_hour > arr_hour) and (dep_minute > arr_minute):
                dur_hour = (dep_hour-arr_hour) + ((arr_day-journey_day)*24)
                dur_minute = dep_minute - arr_minute
            else:
                dur_hour = (arr_hour - dep_hour) + ((arr_day - journey_day) * 24)
                dur_minute = arr_minute - dep_minute


        res = predict_Price(source=source, destination=destination, airline=airline, total_stops=stops,
                            journey_day=journey_day, journey_month=journey_month, dep_hour=dep_hour, dep_min=dep_minute,
                            arr_hour=arr_hour, arr_min=arr_minute, dur_hour=dur_hour, dur_min=dur_minute)
    return render(request, 'result.html', {'res': res})
