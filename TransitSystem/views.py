# Create your views here.
from datetime import datetime


from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from TransitSystem.forms import SearchForm
from models import VehiclePositions, Trips, Routes, StopTimes
from TransitSystem.models import TripUpdates, Stops, CalendarDates
from TransitSystem import gtfs_realtime_pb2
import urllib,traceback
from operator import itemgetter


#use decorator login required if needed
def home(request):
    return render_to_response('index.html')


def findbus(request):
    form=SearchForm(request.POST)
    return render_to_response('findbus.html',{'form':form},context_instance=RequestContext(request))

def searchbus(request):
    try:
        if "routeNo" in request.GET:
            tripdetails=[]
            date=request.GET['searchdate']
            time=request.GET['searchtime']
            date=datetime.strptime(date,'%Y/%m/%d')
            service_id=findserviceId(date) #serviceid is calculated based on day of the week 
            routes=Routes.objects.filter(route_short_name=request.GET['routeNo'])
            for route in routes:
                trips=Trips.objects.filter(route_id=route.route_id,service_id__in=service_id)
                for trip in trips:
                    result={}
                    stops=StopTimes.objects.filter(trip_id=trip.trip_id,stop_sequence=1,arrival_time__gt=time) #stop sequence 1 is used to determine start pointing of the trip
                    for stop in stops:
                        result['tripName']=trip.trip_headsign
                        result['trip_id']=trip.trip_id
                        result['startTime']=stop.arrival_time
                    if result:
                        tripdetails.append(result)
        return render_to_response('results.html',{'stop_times':tripdetails})
    except:
        e = traceback.format_exc()
        return render_to_response('error.html',{'error':e})

def schedule(request):
    try:
        if "trip_id" in request.GET:
            stoptimes=[]
            trip_id=request.GET['trip_id']
            schedules=StopTimes.objects.filter(trip_id=trip_id)
            for schedule in schedules:
                stoptime={}
                print schedule.stop_id
                stoptime["stop_name"]=schedule.stop_id.stop_name
                stoptime["arrival_time"]=schedule.arrival_time
                stoptime["departure_time"]=schedule.departure_time
                stoptimes.append(stoptime)
        return render_to_response('schedule.html',{'stoptimes':stoptimes})
    except:
        e = traceback.format_exc()
        return render_to_response('error.html',{'error':e})

def locate(request):
    try:
        trip_id=request.GET['trip_id']
        stoplocs=StopTimes.objects.filter(trip_id=trip_id)
        if stoplocs:
            stop_locations=[]
            for stoploc in stoplocs:
                stops={}
                stops['lat']=stoploc.stop_id.stop_lat
                stops['lon']=stoploc.stop_id.stop_lon
                stop_locations.append(stops)
        vp=VehiclePositions.objects.filter(trip_id=trip_id)
        vehiclepos={}
        if vp:
            vehicleposition=vp[0];
            vehiclepos['lat']=vehicleposition.p_latitude
            vehiclepos['lon']=vehicleposition.p_longitude
        return render_to_response('locate.html',{'stoplocations':stop_locations,'vp':vehiclepos})
    except:
        e = traceback.format_exc()
        return render_to_response('error.html',{'error':e})

def predict(request):
    try:
        if "trip_id" in request.GET:
            stoptimes=[]
            trip_id=request.GET['trip_id']
            schedules=TripUpdates.objects.filter(trip_id=trip_id)
            for schedule in schedules:
                stoptime={}
                stoptime["stop_name"]=schedule.stop_id.stop_name
                stoptime["arrival_time"]=schedule.arrival_time
                stoptime["departure_time"]=schedule.departure_time
                stoptimes.append(stoptime)
        return render_to_response('predictions.html',{'stoptimes':stoptimes})
    except:
        e = traceback.format_exc()
        return render_to_response('error.html',{'error':e})
def findserviceId(date):
    date=date.date()
    result=[]
    dayofweek=date.weekday()
    if (dayofweek>=0 and dayofweek<5):
        result.append(1)
    else:
        result.append(80)
    service_ids=CalendarDates.objects.filter(date=datetime.strftime(date,'%Y%m%d'),exception_type=1)
    for service_id in service_ids:
        result.append(service_id.service_id.service_id)
    return result    
