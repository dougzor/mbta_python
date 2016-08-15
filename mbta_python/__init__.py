import datetime
import requests
from mbta_python.models import Stop, Direction, Schedule, Mode, \
    TripSchedule, Alert, StopWithMode, Prediction


HOST = "http://realtime.mbta.com/developer/api/v2"


def datetime_to_epoch(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


class MBTASDK(object):
    """Wrapper around calls to the MBTA Realtime API
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, path, params):
        url = "{}/{}".format(HOST, path)
        response = requests.get(url, params=params)

        data = response.json()

        error = data.get("error")
        if error:
            raise Exception(error["message"])

        return response.json()

    def get_stops_by_location(self, latitude, longitude):
        """Get a List of Stops sorted by proximity to the given
        latitude and longitude
        """
        params = {
            "lat": latitude,
            "lon": longitude,
            "api_key": self.api_key,
            "format": "json"
        }

        data = self._make_request("stopsbylocation", params)

        stops = [Stop(stop_data) for stop_data in data["stop"]]

        return stops

    def get_stops_by_route(self, route_id):
        """Return a List of Directions for the route_id
        that contain a list of Stops that Direction and Route serve
        """
        params = {
            "route": route_id,
            "api_key": self.api_key,
            "format": "json"
        }

        data = self._make_request("stopsbyroute", params)

        return [Direction(d) for d in data["direction"]]

    def get_routes_by_stop(self, stop_id):
        """Return a list of routes that serve a particular stop
        """
        params = {
            "stop": stop_id,
            "api_key": self.api_key,
            "format": "json"
        }
        data = self._make_request("routesbystop", params)

        return StopWithMode(data)

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
        params = {
            "stop": stop_id,
            "api_key": self.api_key,
            "format": "json",
            "route": route_id,
            "direction": direction_id,
            "datetime": datetime_to_epoch(date) if date else None,
            "max_time": max_time,
            "max_trips": max_trips
        }

        data = self._make_request("schedulebystop", params)

        return Schedule(data)

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
        if not isinstance(route_ids, list):
            route_ids = [route_ids]

        params = {
            "routes": ",".join(route_ids),
            "api_key": self.api_key,
            "format": "json",
            "datetime": datetime_to_epoch(date) if date else None,
            "max_time": max_time,
            "max_trips": max_trips
        }
        data = self._make_request("schedulebyroutes", params)

        return [Mode(m) for m in data["mode"]]

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
        params = {
            "trip": trip_id,
            "api_key": self.api_key,
            "format": "json",
            "datetime": datetime_to_epoch(date) if date else None,
        }
        data = self._make_request("schedulebytrip", params)

        return TripSchedule(data)

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
        params = {
            "stop": stop_id,
            "api_key": self.api_key,
            "format": "json",
            "include_access_alerts": include_access_alerts,
            "include_service_alerts": include_service_alerts
        }
        data = self._make_request("predictionsbystop", params)

        return Prediction(data)

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
        if not isinstance(route_ids, list):
            route_ids = [route_ids]

        params = {
            "routes": ",".join(route_ids),
            "api_key": self.api_key,
            "format": "json",
            "include_access_alerts": include_access_alerts,
            "include_service_alerts": include_service_alerts
        }
        data = self._make_request("predictionsbyroutes", params)

        return Prediction(data)

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
        if not isinstance(route_ids, list):
            route_ids = [route_ids]

        params = {
            "routes": ",".join(route_ids),
            "api_key": self.api_key,
            "format": "json",
            "include_access_alerts": include_access_alerts,
            "include_service_alerts": include_service_alerts
        }
        data = self._make_request("vehiclesbyroutes", params)

        return [Mode(m) for m in data]

    def get_predictions_by_trip(self, trip_id):
        """Return the predicted arrivals and departures for a particular trip.
        trip_id - TripID
        """
        params = {
            "trip": trip_id,
            "api_key": self.api_key,
            "format": "json"
        }
        data = self._make_request("predictionsbytrip", params)

        return TripSchedule(data)

    def get_vehicles_by_trip(self, trip_id):
        """Return the predicted vehicle positions for a particular trip.
        trip_id - TripID
        """
        params = {
            "trip": trip_id,
            "api_key": self.api_key,
            "format": "json"
        }
        data = self._make_request("vehiclesbytrip", params)

        return TripSchedule(data)
