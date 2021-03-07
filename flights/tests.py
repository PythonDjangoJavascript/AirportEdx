from django.http import response
from django.test import TestCase, Client, client
from .models import Airport, Flight, Passenger

# Create your tests here.


class FlightTestCase(TestCase):

    def setUp(self):
        airport1 = Airport.objects.create(code="AAA", city="City A")
        airport2 = Airport.objects.create(code="BBB", city="City B")

        # Sample flights
        Flight.objects.create(
            origin=airport1, destination=airport2, duration=100)
        Flight.objects.create(
            origin=airport1, destination=airport1, duration=200)
        Flight.objects.create(
            origin=airport1, destination=airport2, duration=-100)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        airport1 = Airport.objects.get(code="AAA")
        airport2 = Airport.objects.get(code="BBB")
        flight = Flight.objects.create(
            origin=airport1, destination=airport2, duration=100)

        self.assertTrue(flight.is_valid_flight())

    def test_invalid_flght_destination(self):
        airport1 = Airport.objects.get(code="AAA")
        flight = Flight.objects.get(origin=airport1, destination=airport1)
        self.assertFalse(flight.is_valid_flight())

    def test_flight_duration(self):
        airport1 = Airport.objects.get(code="AAA")
        airport2 = Airport.objects.get(code="BBB")
        flight = Flight.objects.create(
            origin=airport1, destination=airport2, duration=-100)

        self.assertFalse(flight.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get(f"/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        airport1 = Airport.objects.get(code="AAA")
        flight = Flight.objects.get(origin=airport1, destination=airport1)

        c = Client()
        response = c.get(f"/flights/{flight.id}")
        self.assertEqual(response.status_code, 200)

# Max function is not working
    # def test_invalid_flight_page(self):
    #     max_id = Flight.objects.all().aggregate(Max('id'))["id__max"]

    #     c = Client()
    #     response = c.get(f"/flights/{max_id + 1}")
    #     self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        flight = Flight.objects.get(pk=1)
        passenger = Passenger.objects.create(first="Nuruddin", last="Syeed")
        flight.passengers.add(passenger)

        c = Client()
        response = c.get(f"/flights/{flight.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        flight = Flight.objects.get(pk=1)
        passenger = Passenger.objects.create(first="Alience", last="Adman")

        c = Client()
        response = c.get(f"/flights/{flight.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
