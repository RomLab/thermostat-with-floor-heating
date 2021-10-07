
import csv
import datetime
 
import pandas
import os
 
import numpy as np
import matplotlib.pyplot as plt

class LinearAprroximation():

    slope = None
    intercept = None
    def create_line(self, numberFloor, heater, sensor):  

        inside,outside,heater = self.read_data(numberFloor, heater, sensor)
       
        durations = self.find_heatup_durations(heater)
        outside_temps = self.find_temperatures_at_times(outside, durations)
        inside_temps = self.find_temperatures_at_times(inside, durations)
        #self.log(durations)
        #self.log(outside_temps)
        #self.log(inside_temps)
        # durations nesmi byt prazdne
        self.analyze_heatups(durations, outside_temps, inside_temps, numberFloor, sensor)
        return self.slope, self.intercept
    
    def read_data(self, numberFloor, heater, sensor):
        inside = pandas.read_csv('/home/appdaemon/.appdaemon/conf/apps/data/temperature_inside/'+numberFloor+'/'+sensor+'.csv', parse_dates=[0],names=['Time','Temperature'],index_col=0)
        inside = inside[inside>-1000] # filter crap readings
        outside = pandas.read_csv('/home/appdaemon/.appdaemon/conf/apps/data/sensor.outdoor.csv', parse_dates=[0],names=['Time','Temperature'],index_col=0)
        heater = pandas.read_csv('/home/appdaemon/.appdaemon/conf/apps/data/heater/'+numberFloor+'/'+heater+'.csv', parse_dates=[0],names=['Time','Status'],index_col=0)
        return inside, outside, heater
 
    def find_heatup_durations(self, heater, status='off'):
        """Figure out how long the heater was on for each morning."""
        last_time = next(heater.iterrows())[0]
        heatup_durations = []
        for time, df in heater.iterrows():
            diff = time - last_time
            if df['Status']==status and diff > datetime.timedelta(hours=1):
                heatup_durations.append((last_time, diff)) # remember when it turned on too
            last_time = time
        return heatup_durations
    
    def find_temperatures_at_times(self, temperatures, times):
        """Find what the temperature was during the morning heatup."""
        blocks = []
        for start_time, duration in times:
            blocks.append((start_time, temperatures[start_time: start_time + duration]))
        return blocks
    
    def analyze_heatups(self, durations, outside_temps, inside_temps, numberFloor, sensor):
        """Look at the heatup dynamics and try to build a model."""
        initial_outside = np.array([o[1].values[0] for o in outside_temps])
        initial_inside = np.array([o[1].values[0] for o in inside_temps])
        durations_in_minutes = np.array([d[1].total_seconds() for d in durations])/60.0
        delta = (initial_inside-initial_outside)[:,0]
        print(delta)
        self.slope, self.intercept = np.polyfit(delta, durations_in_minutes,1)
 
        model_temp = np.linspace(min(delta), max(delta), 20)
        model_duration = self.slope * model_temp + self.intercept

       
    
        plt.figure()
        ax = plt.gca()
        #plt.plot(initial_outside, durations_in_seconds,'o')
        plt.plot(delta, durations_in_minutes,'o', label='Data')
        plt.plot(model_temp, model_duration,'-', label='Model')
        plt.text(0.2,0.1,'D = {:.1f} T + {:.1f}'.format(self.slope, self.intercept), transform = ax.transAxes)
        plt.xlabel('Initial delta Temperature (C)')
        plt.ylabel('Duration of heatup (min)')
        plt.title('Duration of heatups')
        #os.chmod('/home/appdaemon/.appdaemon/conf/apps/heatups.png', 0o400)
        plt.savefig('/home/appdaemon/.appdaemon/conf/apps/data/temperature_inside/'+numberFloor+'/'+sensor+'.png')