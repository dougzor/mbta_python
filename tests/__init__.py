import unittest

TEST_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


class MockResponse(object):

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


class MBTATests(unittest.TestCase):

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
