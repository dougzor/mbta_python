import requests
from mbta_python.models import Stop, Direction, StopWithMode, Mode, \
    TripSchedule, Alert


HOST = "http://realtime.mbta.com/developer/api/v2"


def datetime_to_epoch(dt):
    return None


class MBTASDK(object):
    """Wrapper around calls to the MBTA Realtime API
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stops_by_location(self, latitude, longitude):
        """Get a List of Stops sorted by proximity to the given
        latitude and longitude
        """
        url = "{}/stopsbylocation".format(HOST)
        params = {
            "lat": latitude,
            "lon": longitude,
            "api_key": self.api_key,
            "format": "json"
        }

        response = requests.get(url, params=params)

        stops = [Stop(stop_data) for stop_data in response.json()["stop"]]

        return stops

    def get_stops_by_route(self, route_id):
        """Return a List of Directions for the route_id
        that contain a list of Stops that Direction and Route serve
        """
        url = "{}/stopsbyroute".format(HOST)
        params = {
            "route_id": route_id,
            "api_key": self.api_key,
            "format": "json"
        }

        response = requests.get(url, params=params)

        return [Direction(d) for d in response.json()["direction"]]

    def get_routes_by_stop(self, stop_id, include_schedules=False):
        """Return a list of routes that serve a particular stop
        """
        url = "{}/routesbystop".format(HOST)
        params = {
            "stop": stop_id,
            "api_key": self.api_key,
            "format": "json"
        }
        response = requests.get(url, params=params)

        return StopWithMode(response.json())

    def get_schedules_by_stop(self, stop_id, route_id=None, direction_id=None,
                              date=None, max_time=None, max_trips=None):
        """Return scheduled arrivals and departures for a direction and route for a
        particular stop.

        stop_id - Stop ID
        route_id - Route ID, If not included then schedule for all routes
                   serving the stop will be returned,
        direction_id - Direction ID, If included then route must also be
                       included if not included then schedule for all
                       directions of the route serving the stop will be
                       returned
        date - Time after which schedule should be returned. If included
               then must be within the next seven (7) days
               If not included then schedule starting from the current
               datetime will be returned
        max_time - Defines maximum range of time (in minutes) within which
                   trips will be returned. If not included defaults to 60.
        max_trips - Defines number of trips to return. Integer between 1 and
                    100. If not included defaults to 5.
        """
        url = "{}/schedulebystop".format(HOST)
        params = {
            "stop": stop_id,
            "api_key": self.api_key,
            "format": "json",
            "route": route_id,
            "direction": direction_id,
            "datetime": date,
            "max_time": max_time,
            "max_trips": max_trips
        }

        response = requests.get(url, params=params)

        return StopWithMode(response.json())

    def get_schedules_by_routes(self, route_ids, date=None,
                                max_time=None, max_trips=None):
        """Return the scheduled arrivals and departures in a direction
        for a particular route or routes.

        route_ids - List of Route IDs, or single Route ID
        date - Time after which schedule should be returned. If included
               then must be within the next seven (7) days If not included
               then schedule starting from the current datetime will
               be returned
        max_time - Defines maximum range of time (in minutes) within which
                   trips will be returned. If not included defaults to 60.
        max_trips - Defines number of trips to return. Integer between 1
                    and 100. If not included defaults to 5.
        """
        url = "{}/schedulebyroutes".format(HOST)

        if not isinstance(route_ids, list):
            route_ids = list(route_ids)

        params = {
            "routes": ",".join(route_ids),
            "api_key": self.api_key,
            "format": "json",
            "datetime": date,
            "max_time": max_time,
            "max_trips": max_trips
        }
        response = requests.get(url, params=params)

        return [Mode(m) for m in response.json()["mode"]]

    def get_schedules_by_trip(self, trip_id, date=None):
        """Return the scheduled arrivals and departures in a direction
        for a particular route or routes.

        route_ids - List of Route IDs, or single Route ID
        date - Time after which schedule should be returned. If included then
               must be within the next seven (7) days. If not included then
               schedule starting from the current datetime will be returned
        max_time - Defines maximum range of time (in minutes) within which
                   trips will be returned. If not included defaults to 60.
        max_trips - Defines number of trips to return. Integer between 1 and
                    100. If not included defaults to 5.
        """
        url = "{}/schedulebytrip".format(HOST)

        params = {
            "trip": trip_id,
            "api_key": self.api_key,
            "format": "json",
            "datetime": date
        }
        response = requests.get(url, params=params)

        return TripSchedule(response.json())

    def get_predictions_by_stop(self, stop_id, include_access_alerts=False,
                                include_service_alerts=True):
        """Return predicted arrivals and departures in the next hour for a
        direction and route for a particular stop.

        stop_id - Stop ID
        include_access_alerts - Whether or not alerts pertaining to
                                accessibility (elevators, escalators) should be
                                returned
        include_service_alerts - Whether or not service alerts should be
                                 returned
        """
        url = "{}/predictionsbystop".format(HOST)

        params = {
            "stop": stop_id,
            "api_key": self.api_key,
            "format": "json",
            "include_access_alerts": include_access_alerts,
            "include_service_alerts": include_service_alerts
        }
        response = requests.get(url, params=params)

        return StopWithMode(response.json())

    def get_predictions_by_routes(self, route_ids, include_access_alerts=False,
                                  include_service_alerts=True):
        """Return predictions for upcoming trips (including trips already underway)
        in a direction for a particular route or routes.

        route_ids - List of Route IDs, or single Route ID
        include_access_alerts - Whether or not alerts pertaining to
                                accessibility (elevators, escalators) should be
                                returned
        include_service_alerts - Whether or not service alerts should be
                                 returned
        """
        url = "{}/predictionsbyroutes".format(HOST)
        if not isinstance(route_ids, list):
            route_ids = list(route_ids)

        params = {
            "routes": ",".join(route_ids),
            "api_key": self.api_key,
            "format": "json",
            "include_access_alerts": include_access_alerts,
            "include_service_alerts": include_service_alerts
        }
        response = requests.get(url, params=params)

        modes = [Mode(m) for m in response.json["mode"]]
        alerts = [Alert(a) for a in response.json["alert_headers"]]

        return modes, alerts

    def get_vehicles_by_routes(self, route_ids, include_access_alerts=False,
                               include_service_alerts=True):
        """Return vehicle positions for upcoming trips (including trips already
        underway) in a direction for a particular route or routes.

        route_ids - List of Route IDs, or single Route ID
        include_access_alerts - Whether or not alerts pertaining to
                                accessibility (elevators, escalators) should be
                                returned
        include_service_alerts - Whether or not service alerts should be
                                 returned
        """
        url = "{}/vehiclesbyroutes".format(HOST)
        if not isinstance(route_ids, list):
            route_ids = list(route_ids)

        params = {
            "routes": ",".join(route_ids),
            "api_key": self.api_key,
            "format": "json",
            "include_access_alerts": include_access_alerts,
            "include_service_alerts": include_service_alerts
        }
        response = requests.get(url, params=params)

        return [Mode(m) for m in response.json["mode"]]

    def get_predictions_by_trip(self, trip_id):
        """Return the predicted arrivals and departures for a particular trip.
        trip_id - TripID
        """
        url = "{}/predictionsbytrip".format(HOST)

        params = {
            "trip": trip_id,
            "api_key": self.api_key,
            "format": "json"
        }
        response = requests.get(url, params=params)

        return TripSchedule(response.json())

    def get_vehicles_by_trip(self, trip_id):
        """Return the predicted vehicle positions for a particular trip.
        trip_id - TripID
        """
        url = "{}/vehiclesbytrip".format(HOST)

        params = {
            "trip": trip_id,
            "api_key": self.api_key,
            "format": "json"
        }
        response = requests.get(url, params=params)

        return TripSchedule(response.json())
