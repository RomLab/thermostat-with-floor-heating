import appdaemon.plugins.hass.hassapi as hass
import os
import re
from glob import glob
import time
import datetime
from datetime import timedelta
import RPi.GPIO as GPIO

class READTHERMOSTAT(hass.Hass):

    def initialize(self):
        interval_of_reading = 1
        start_time = self.datetime() + datetime.timedelta(seconds = 1)
        self.handle = self.run_every(self.read_thermostat, start_time, interval_of_reading)

    def read_thermostat(self, kwargs): 
        GPIO.setmode(GPIO.BCM) 
        
        GPIO.setup(24, GPIO.IN) 
        state_first_floor = GPIO.input(24)
        
        GPIO.setup(23, GPIO.IN) 
        state_second_floor = GPIO.input(23)
        
        states_thermostat_first_floor = self.get_state("sensor.thermostat_first_floor", attribute='all')
        attributes_thermostat_first_floor = states_thermostat_first_floor['attributes']
        self.set_state("sensor.thermostat_first_floor", state = state_first_floor, attributes = attributes_thermostat_first_floor)

        states_thermostat_second_floor = self.get_state("sensor.thermostat_second_floor", attribute='all')
        attributes_thermostat_second_floor = states_thermostat_second_floor['attributes']
        self.set_state("sensor.thermostat_second_floor", state = state_second_floor, attributes = attributes_thermostat_second_floor)
    