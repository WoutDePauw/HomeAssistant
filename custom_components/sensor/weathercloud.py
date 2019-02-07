"""
Add this file to <config-dir>/custom_components/sensor/

configuration.yaml:

sensor:
  - platform: weathercloud
    station_id: <station id>

"""

from homeassistant.util import Throttle
from homeassistant.const import (CONF_NAME)
from homeassistant.helpers.entity import Entity
import requests

BASE_URL = 'https://app.weathercloud.net/device/values?code='
CONF_ID = 'station_id'
HEADERS = {'X-Requested-With':'XMLHttpRequest'}

def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup the sensor platform."""
	station_id = config.get(CONF_ID)
	add_devices([Weathercloud(station_id)])


class Weathercloud(Entity):
	"""Representation of a Sensor."""

	def __init__(self, station_id):
		"""Initialize the sensor."""
		self._state = None
		self._id = station_id
	@property
	def name(self):
		"""Return the name of the sensor."""
		return 'Weathercloud sensor'

	@property
	def state(self):
		"""Return the state of the sensor."""
		return self._state

	@property
	def id(self):
		"""return station id"""
		return self._id

	def update(self):
		"""Fetch new state data for the sensor.

		This is the only method that should fetch new data for Home Assistant.
		"""

		#try:
		r=requests.get(BASE_URL + str(self._id) , verify=False, headers=HEADERS)

		resp = r.json()
		self._state = resp
		#except:
		#	self._state = "could not get status"
		#	return
