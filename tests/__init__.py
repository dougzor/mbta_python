import unittest
import datetime

TEST_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


class MockResponse(object):

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


class MBTATests(unittest.TestCase):

    @property
    def next_wednesday(self):
        """Helper to get the next wednesday - when there will
        probably be an actual departure
        """
        now = datetime.datetime.utcnow()
        now = now.replace(hour=13, minute=0, second=0)  # 8 or 9am EST

        while now.date().weekday() != 2:
            now = now + datetime.timedelta(days=1)

        return now

    def test_get_routes_by_stop(self):
        from mbta_python import MBTASDK
        from mbta_python.models import StopWithMode
        sdk = MBTASDK(TEST_API_KEY)

        schedule = sdk.get_routes_by_stop("place-alfcl")

        self.assertIsInstance(schedule, StopWithMode)

    def test_get_stops_by_location(self):
        from mbta_python import MBTASDK
        from mbta_python.models import Stop
        sdk = MBTASDK(TEST_API_KEY)

        stops = sdk.get_stops_by_location(42.395263, -71.142555)

        for stop in stops:
            self.assertIsInstance(stop, Stop)
            if stop.stop_id == "place-alfcl":
                break
        else:
            self.assertTrue(False, "Didn't find Alewife")

    def test_get_stops_by_route(self):
        from mbta_python import MBTASDK
        from mbta_python.models import Direction
        sdk = MBTASDK(TEST_API_KEY)

        directions = sdk.get_stops_by_route("Red")

        for direction in directions:
            self.assertIsInstance(direction, Direction)

    def test_get_schedules_by_stop(self):
        from mbta_python import MBTASDK
        from mbta_python.models import Schedule
        sdk = MBTASDK(TEST_API_KEY)

        schedule = sdk.get_schedules_by_stop("place-alfcl",
                                             direction_id="1")

        self.assertIsInstance(schedule, Schedule)

    def test_get_schedules_by_routes(self):
        from mbta_python import MBTASDK
        from mbta_python.models import Mode
        sdk = MBTASDK(TEST_API_KEY)

        schedules = sdk.get_schedules_by_routes(
            ["116", "117"],
            date=self.next_wednesday
        )

        for schedule in schedules:
            self.assertIsInstance(schedule, Mode)
