"""
Add this file to <config-dir>/custom_components/sensor/

configuration.yaml:

sensor:
  - platform: weathercloud
    station_id: <station id>

"""

from homeassistant.util import Throttle
from homeassistant.const import (ATTR_ATTRIBUTION, CONF_NAME)
from homeassistant.helpers.entity import Entity
from datetime import datetime
import requests
BASE_URL = 'https://www.ophaalkalender.be/api/rides?housenumber=0&id='
ID_URL = 'https://www.ophaalkalender.be/calendar/findstreets?query='
CONF_POSTAL = 'zip_code'
CONF_STREET = 'street_name'
HEADERS = {'X-Requested-With':'XMLHttpRequest'}
TIMEFORMAT = '%Y-%m-%d'
DEFAULT_ATTRIBUTION = 'Please Recyle'
def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup the sensor platform."""
	zip_code = config.get(CONF_POSTAL)
	street = config.get(CONF_STREET)
	add_devices([Recyle(zip_code, street)])


class Recyle(Entity):
	"""Representation of a Sensor."""

	def __init__(self, zip_code, street):
		"""Initialize the sensor."""
		self._state = None
		self._zipcode = zip_code
		self._street = street
		self._attrs = {ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION}
		self.getID()
		self.update()
	@property
	def device_state_attributes(self):
		"""return the device state attributes"""
		return self._attrs

	@property
	def name(self):
		"""Return the name of the sensor."""
		return 'Recycle sensor'

	@property
	def state(self):
		"""Return the state of the sensor."""
		return self._state

	@property
	def id(self):
		"""return station id"""
		return self._id

	def getID(self):
		"""gets ID for calendar filtering"""
		r=requests.get(ID_URL + str(self._street) + '&zipcode=' + str(self._zipcode) , verify=False, headers=HEADERS)
		self._id = r.json()[0]['Id']
		self._attrs.update({
			'Id': self._id
		})

	def update(self):
		"""Fetch new state data for the sensor.

		This is the only method that should fetch new data for Home Assistant.
		"""

		#try:
		r=requests.get(BASE_URL + str(self._id) + '&zipcode=' + str(self._zipcode) , verify=False, headers=HEADERS)
		resp = r.json()
		events = {}
		now = datetime.now()
		counter = 0
		for item in resp:
			then = datetime.strptime(item['start'][:-15], TIMEFORMAT)
			if ( then >= now):
				events[counter] = item
				counter += 1
				if counter >= 10:
					break
		self._attrs.update(events)
		"""self._state = resp"""
		#except:
		#	self._state = "could not get status"
		#	return
