from __future__ import unicode_literals
from django.db import models

class Agency(models.Model):
    agency_id = models.CharField(max_length=11L, primary_key=True)
    agency_name = models.CharField(max_length=255L, blank=True)
    agency_url = models.CharField(max_length=255L, blank=True)
    agency_timezone = models.CharField(max_length=50L, blank=True)
    agency_lang = models.CharField(max_length=255L, blank=True)
    agency_phone = models.CharField(max_length=15L, blank=True)
    agency_fare_url = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'agency'

class Calendar(models.Model):
    service_id = models.IntegerField(primary_key=True)
    monday = models.IntegerField(null=True, blank=True)
    tuesday = models.IntegerField(null=True, blank=True)
    wednesday = models.IntegerField(null=True, blank=True)
    thursday = models.IntegerField(null=True, blank=True)
    friday = models.IntegerField(null=True, blank=True)
    saturday = models.IntegerField(null=True, blank=True)
    sunday = models.IntegerField(null=True, blank=True)
    start_date = models.CharField(max_length=8L, blank=True)
    end_date = models.CharField(max_length=8L, blank=True)
    start_date_timestamp = models.IntegerField(null=True, blank=True)
    end_date_timestamp = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'calendar'

class CalendarDates(models.Model):
    service_id = models.ForeignKey(Calendar,db_column='service_id')
    date = models.CharField(max_length=8L, blank=True)
    exception_type = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'calendar_dates'

class Routes(models.Model):
    route_id = models.IntegerField(primary_key=True)
    agency_id = models.ForeignKey(Agency,db_column='agency_id')
    route_short_name = models.CharField(max_length=50L, blank=True)
    route_long_name = models.CharField(max_length=255L, blank=True)
    route_type = models.IntegerField(null=True, blank=True)
    route_text_color = models.CharField(max_length=255L, blank=True)
    route_color = models.CharField(max_length=255L, blank=True)
    route_url = models.CharField(max_length=255L, blank=True)
    route_desc = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'routes'

class Trips(models.Model):
    route_id = models.ForeignKey(Routes,db_column='route_id')
    service_id = models.ForeignKey(Calendar,db_column='service_id')
    trip_id = models.IntegerField(primary_key=True)
    trip_headsign = models.CharField(max_length=255L, blank=True)
    trip_short_name = models.CharField(max_length=255L, blank=True)
    direction_id = models.IntegerField(null=True, blank=True)
    block_id = models.IntegerField(null=True, blank=True)
    shape_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'trips'

class Stops(models.Model):
    stop_id = models.IntegerField(primary_key=True)
    stop_code = models.CharField(max_length=50L, blank=True)
    stop_name = models.CharField(max_length=255L, blank=True)
    stop_desc = models.CharField(max_length=255L, blank=True)
    stop_lat = models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)
    stop_lon = models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)
    zone_id = models.IntegerField(null=True, blank=True)
    stop_url = models.CharField(max_length=255L, blank=True)
    location_type = models.IntegerField(null=True, blank=True)
    parent_station = models.IntegerField(null=True, blank=True)
    wheelchair_boarding = models.CharField(max_length=2L, blank=True)
    class Meta:
        db_table = 'stops'

class StopTimes(models.Model):
    trip_id = models.ForeignKey(Trips,db_column='trip_id')
    arrival_time = models.TimeField(auto_now=False)
    departure_time = models.TimeField(auto_now=False)
    stop_id = models.ForeignKey(Stops,db_column='stop_id') #shud be made foreign key
    stop_sequence = models.IntegerField(null=True, blank=True)
    stop_headsign = models.CharField(max_length=50L, blank=True)
    pickup_type = models.IntegerField(null=True, blank=True)
    drop_off_type = models.IntegerField(null=True, blank=True)
    shape_dist_traveled = models.CharField(max_length=50L, blank=True)
    class Meta:
        db_table = 'stop_times'


class VehiclePositions(models.Model):
    trip_id=models.ForeignKey(Trips,db_column='trip_id')
    route_id=models.ForeignKey(Routes,db_column='route_id',null=True)
    vehicle_id=models.CharField(max_length=255L)
    p_latitude=models.DecimalField(null=True,blank=True,decimal_places=10,max_digits=12)
    p_longitude=models.DecimalField(null=True,blank=True,decimal_places=10,max_digits=12)
    p_bearing=models.DecimalField(null=True,blank=True,decimal_places=10,max_digits=12)
    p_speed=models.DecimalField(null=True,blank=True,decimal_places=10,max_digits=12)
    class Meta:
        db_table='VehiclePositions'


class TripUpdates(models.Model):
    trip_id=models.ForeignKey(Trips,db_column='trip_id')
    stop_id = models.ForeignKey(Stops,db_column='stop_id') #shud be made foreign key
    stop_sequence = models.IntegerField(null=True, blank=True)
    arrival_time=models.TimeField(auto_now=False)
    departure_time=models.TimeField(auto_now=False)
    timestamp=models.TimeField(auto_now=False)
    class Meta:
        db_table='TripUpdates'

