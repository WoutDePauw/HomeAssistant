"""
Add this file to <config-dir>/custom_components/sensor/

configuration.yaml:

sensor:
  - platform: bpost
    token: <parcel code>

"""

from homeassistant.util import Throttle
from homeassistant.const import (CONF_NAME, CONF_TOKEN)
from homeassistant.helpers.entity import Entity
import requests

BASE_URL = 'https://track.bpost.be/btr/api/items?itemIdentifier='

def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup the sensor platform."""
	parcel_code = config.get(CONF_TOKEN)
	add_devices([ExampleSensor(parcel_code)])


class ExampleSensor(Entity):
	"""Representation of a Sensor."""

	def __init__(self, parcel_code):
		"""Initialize the sensor."""
		self._state = None
		self._code = parcel_code
	@property
	def name(self):
		"""Return the name of the sensor."""
		return 'Bpost parcel tracker'

	@property
	def state(self):
		"""Return the state of the sensor."""
		return self._state

	@property
	def code(self):
		"""return parcel tracking code"""
		return self._code

	def update(self):
		"""Fetch new state data for the sensor.

		This is the only method that should fetch new data for Home Assistant.
		"""

		try:
			r = requests.get(BASE_URL + self._code)
			resp = r.json()
			state = resp['items'][0]['processOverview']['activeStepTextKey']
			self._state = state
		except:
			self._state = "could not get status"
			return
