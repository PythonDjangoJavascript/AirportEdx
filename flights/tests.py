from django.http import response
from django.test import TestCase, Client, client
from .models import Airport, Flight, Passenger

# Create your tests here.


class FlightTestCase(TestCase):

    def setUp(self):
        airport1 = Airport.objects.create(code="AAA", city="City A")
        airport2 = Airport.objects.create(code="BBB", city="City B")

        # Flights
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
        valid_flight = Flight.objects.create(
            origin=airport1, destination=airport2, duration=100)

        self.assertTrue(valid_flight.is_valid_flight())

    def test_invalid_flight_destination(self):
        airport1 = Airport.objects.get(code="AAA")
        invalid_destination_flight = Flight.objects.create(
            origin=airport1, destination=airport1, duration=200)

        self.assertFalse(invalid_destination_flight.is_valid_flight())

    def test_invalid_fight_duration(self):
        airport1 = Airport.objects.get(code="AAA")
        airport2 = Airport.objects.get(code="BBB")
        invalid_duration_flight = Flight.objects.create(
            origin=airport1, destination=airport2, duration=-100)

        self.assertFalse(invalid_duration_flight.is_valid_flight())

# Server Request Validation:

    def test_index_page(self):
        client = Client()
        response = client.get("/flights/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flights_page(self):
        valid_flight = Flight.objects.get(pk=1)

        client = Client()
        response = client.get(f"/flights/{valid_flight.id}")

        self.assertEqual(response.status_code, 200)

    # Max function is not working
        # def test_invalid_flight_page(self):
        #     max_id = Flight.objects.all().aggregate(Max('id'))["id__max"]

        #     c = Client()
        #     response = c.get(f"/flights/{max_id + 1}")
        #     self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        valid_flight = Flight.objects.get(pk=1)
        passenger_one = Passenger.objects.create(
            first="Nuruddin", last="Syeed")
        valid_flight.passengers.add(passenger_one)

        client = Client()
        response = client.get((f"/flights/{valid_flight.id}"))
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        valid_flight = Flight.objects.get(pk=1)
        passenger_two = Passenger.objects.create(
            first="Alienvce", last="Adnan")

        client = Client()
        response = client.get(f"/flights/{valid_flight.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
