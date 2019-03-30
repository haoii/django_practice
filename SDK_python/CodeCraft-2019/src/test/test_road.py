
import unittest
from dispatcher.road import HalfRoad, Road
from dispatcher.car import CarStatus, Car
from dispatcher.cross import Cross


roads = [
    Road(5000, 15, 6, 2, 1, 2, 1),
    Road(5001, 18, 4, 2, 2, 3, 1),
    Road(5002, 20, 6, 1, 3, 4, 1),
    Road(5003, 18, 8, 2, 4, 5, 1),
    Road(5004, 18, 4, 1, 5, 6, 1),
    Road(5005, 18, 8, 3, 6, 7, 1),
    Road(5006, 12, 6, 2, 7, 8, 1),
    Road(5007, 20, 8, 4, 1, 9, 1),
    Road(5008, 12, 6, 4, 2, 10, 1),
    Road(5009, 20, 4, 4, 3, 11, 1),
]

cars = [
    Car(10000, 18, 50, 8, 3),
    Car(10001, 51, 3, 8, 4),
    Car(10002, 24, 64, 6, 4),
    Car(10003, 6, 50, 2, 5),
    Car(10004, 20, 62, 2, 7),
    Car(10005, 38, 4, 8, 6),
    Car(10006, 37, 4, 8, 2),
]


class TestRoad(unittest.TestCase):

    def test_print(self):
        half_road = HalfRoad(5000, 15, 6, 2, 1, 2, False)
        half_road.lanes[1][2] = cars[2]
        half_road.lanes[0][4] = cars[3]
        print(half_road)
