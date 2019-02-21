
from django.test import TestCase
from .aeris_weather import simpleAerisRequest

class ErrorsTest(TestCase):

	def test_failed_connection:
		# Use any number for client id
		simpleAerisRequest('97203', 'observations', {}, '12345')
