from schematics.models import Model
from schematics.types import StringType, IntType, BooleanType
from schematics.types.compound import ListType, ModelType


class Stop(Model):
    stop_id = StringType(required=True)
    stop_name = StringType(required=True)
    parent_station = StringType()
    parent_station_name = StringType()
    stop_lat = StringType(required=True)
    stop_lon = StringType(required=True)
    distance = StringType()
    stop_order = StringType()
    sch_arr_dt = IntType()
    sch_dep_dt = IntType()
    stop_sequence = StringType()


class Alert(Model):
    alert_id = StringType(required=True)
    header_text = StringType(required=True)
    effect_name = StringType(required=True)


class Vehicle(Model):
    vehicle_id = StringType(required=True)
    vehicle_lat = StringType(required=True)
    vehicle_lon = StringType(required=True)
    vehicle_bearing = IntType(required=True)
    vehicle_speed = IntType(required=True)
    vehicle_timestamp = IntType(required=True)


class Trip(Model):
    trip_id = StringType(required=True)
    trip_name = StringType(required=True)
    trip_headsign = StringType()

    sch_arr_dt = IntType()
    sch_dep_dt = IntType()

    pre_dt = StringType()
    pre_away = IntType()

    vehicle = ModelType(Vehicle)
    stop = ListType(ModelType(Stop))


class Direction(Model):
    direction_id = StringType(required=True)
    direction_name = StringType(required=True)
    trip = ListType(ModelType(Trip))
    stop = ListType(ModelType(Stop))


class Route(Model):
    route_id = StringType(required=True)
    route_name = StringType(required=True)
    direction = ListType(ModelType(Direction))
    route_hide = BooleanType()


class Mode(Model):
    route_type = StringType(required=True)
    mode_name = StringType(required=True)
    route = ListType(ModelType(Route))


class StopWithMode(Stop):
    mode = ListType(ModelType(Mode))


class Schedule(Model):
    stop_id = StringType(required=True)
    stop_name = StringType(required=True)
    parent_station = StringType()
    parent_station_name = StringType()
    stop_lat = StringType(required=True)
    stop_lon = StringType(required=True)
    distance = StringType()
    stop_order = StringType()
    mode = ListType(ModelType(Mode))
    alert_headers = ListType(ModelType(Alert))


class TripSchedule(Model):
    route_id = StringType(required=True)
    route_name = StringType(required=True)
    trip_id = StringType(required=True)
    trip_name = StringType(required=True)
    direction_id = StringType(required=True)
    direction_name = StringType(required=True)
    stop = ListType(ModelType(Stop))
    vehicle = ModelType(Vehicle)
