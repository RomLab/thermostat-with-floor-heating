import appdaemon.plugins.hass.hassapi as hass
import sys
import psycopg2
from psycopg2 import Error
from linearaprroximation import LinearAprroximation

class DATABASE(hass.Hass):
    def initialize(self):
        self.listen_state(self.trigger, "sensor.current_weekday", new = "Monday")
        #self.listen_state(self.trigger, "input_boolean.manual_winter_mode")

    def trigger(self, entity, attribute, old, new, kwargs):  
        
        aprroximation = LinearAprroximation()

        slopeFirstFloor = [
            "input_number.first_floor_corridor_and_toilet_slope", 
            "input_number.first_floor_bathroom_slope", 
            "input_number.first_floor_living_room_and_kitchen_slope", 
            "input_number.first_floor_cellar_slope",
            "input_number.first_floor_garage_slope"]
        interceptFirstFloor = [
            "input_number.first_floor_corridor_and_toilet_intercept",
            "input_number.first_floor_bathroom_intercept", 
            "input_number.first_floor_living_room_and_kitchen_intercept",
            "input_number.first_floor_cellar_intercept", 
            "input_number.first_floor_garage_intercept"]
        heaterFristFloor = [
            "input_boolean.zone_first_floor_corridor_and_toilet", 
            "input_boolean.zone_first_floor_bathroom", 
            "input_boolean.zone_first_floor_living_room_and_kitchen", 
            "input_boolean.zone_first_floor_cellar", 
            "input_boolean.zone_first_floor_garage"]
        sensorFirstFloor = [
            "sensor.first_floor_corridor_and_toilet_temp",
            "sensor.first_floor_bathroom_temp", 
            "sensor.first_floor_living_room_and_kitchen_temp", 
            "sensor.first_floor_cellar_temp",
            "sensor.first_floor_garage_temp"]

        outdoorSensor = "sensor.outdoor"

        self.getCreateCSVFromDatabese(outdoorSensor, str(outdoorSensor)+".csv")
        
        for index, value in enumerate(slopeFirstFloor):
            self.getCreateCSVFromDatabese(heaterFristFloor[index], "heater/first_floor/"+str(heaterFristFloor[index])+".csv")
            self.getCreateCSVFromDatabese(sensorFirstFloor[index], "temperature_inside/first_floor/"+str(sensorFirstFloor[index])+".csv")
            slope, intercept = aprroximation.create_line("first_floor", heaterFristFloor[index], sensorFirstFloor[index])
            if(slope != None and intercept != None):
                self.set_state(slopeFirstFloor[index],  state = slope)
                self.set_state(interceptFirstFloor[index],  state = intercept)
            else:
                self.log("Problem with slope or intercept for first floor.")

        slopeSecondFloor = [
        "input_number.second_floor_bathroom_slope", 
        "input_number.second_floor_kitchen_workroom_living_and_diving_room_slope", 
        "input_number.second_floor_thomas_bedroom_slope", 
        "input_number.second_floor_north_room_slope", 
        "input_number.second_floor_middle_room_slope", 
        "input_number.second_floor_corner_room_slope", 
        "input_number.second_floor_corridor_and_toilet_room_slope", 
        "input_number.second_floor_parents_bedroom_slope"]

        interceptSecondFloor = [
            "input_number.second_floor_bathroom_intercept", 
            "input_number.second_floor_kitchen_workroom_living_and_diving_room_intercept", 
            "input_number.second_floor_thomas_bedroom_intercept", 
            "input_number.second_floor_north_room_intercept", 
            "input_number.second_floor_middle_room_intercept", 
            "input_number.second_floor_corner_room_intercept", 
            "input_number.second_floor_corridor_and_toilet_room_intercept", 
            "input_number.second_floor_parents_bedroom_intercept"]
        
        heaterSecondFloor = [
            "input_boolean.zone_second_floor_bathroom",
            "input_boolean.zone_second_floor_kitchen_workroom_living_and_diving_room",
            "input_boolean.zone_second_floor_thomas_bedroom",
            "input_boolean.zone_second_floor_north_room",
            "input_boolean.zone_second_floor_middle_room",
            "input_boolean.zone_second_floor_corner_room",
            "input_boolean.zone_second_floor_corridor_and_toilet",
            "input_boolean.zone_second_floor_parents_bedroom"]
        
        sensorSecondFloor = [
            "sensor.second_floor_bathroom_temp",
            "sensor.second_floor_kitchen_workroom_living_and_diving_room_temp",
            "sensor.second_floor_thomas_bedroom_temp",
            "sensor.second_floor_north_room_temp",
            "sensor.second_floor_middle_room_temp",
            "sensor.second_floor_corner_room_temp",
            "sensor.second_floor_corridor_and_toilet_temp",
            "sensor.second_floor_parents_bedroom_temp"]

        for index, value in enumerate(slopeSecondFloor):
            self.getCreateCSVFromDatabese(heaterSecondFloor[index], "heater/second_floor/"+str(heaterSecondFloor[index])+".csv")
            self.getCreateCSVFromDatabese(sensorSecondFloor[index], "temperature_inside/second_floor/"+str(sensorSecondFloor[index])+".csv")
            slope, intercept = aprroximation.create_line("second_floor", heaterSecondFloor[index], sensorSecondFloor[index])
            if(slope != None and intercept != None):
                self.set_state(slopeSecondFloor[index],  state = slope)
                self.set_state(interceptSecondFloor[index],  state = intercept)
            else:
                self.log("Problem with slope or intercept for second floor.")
     

        
    
    def getCreateCSVFromDatabese(self, entity, path):
        connection = None
        try:
            # Connect to an existing database
            connection = psycopg2.connect(user="appdaemon",
                                          password="VelmiSilneHesloProHomeassistant",
                                          host="localhost",
                                          port="5432",
                                          database="homeassistant")  
            # Create a cursor to perform database operations
            cursor = connection.cursor()
             #self.log("TESTTEST222")
            sql = "COPY (SELECT last_updated, state from states WHERE entity_id="+"'"+str(entity)+"' ORDER BY last_updated ASC) TO STDOUT WITH CSV DELIMITER ','"
            #outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format("SELECT last_updated, state from states WHERE entity_id='switch.blue_led'")
            with open("home/appdaemon/.appdaemon/conf/apps/data/"+str(path), 'w') as f:
                cursor.copy_expert(sql, f)
            # Print PostgreSQL details
            #print("PostgreSQL server information")
            #print(connection.get_dsn_parameters(), "\n")
            # Executing a SQL query SELECT current_database()
            #cursor.execute("SELECT * from states;")
            # Fetch result
            #record = cursor.fetchone()
            #self.log("You are connected to - ", record, "\n")  

            #cursor.execute("SELECT last_updated, state from states WHERE entity_id='sensor.hot_water_tank_top'")
            #record = cursor.fetchall()
           # self.log(record)

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")




    def getEntityHeater(self, typeOfEntity):
        
        listEntity = []
        for entity in self.get_state("input_boolean"):
            if typeOfEntity in entity:
                listEntity.append(entity)
        
        return listEntity
    
    def getSensorFromRoom(self, floorNumber):
        
        listEntity = []

        for entity in self.get_state("sensor"):
            if floorNumber in entity:
                splitEntity = entity.split("_")
                if splitEntity[-1] == "temp":
                    listEntity.append(entity)
        
        return listEntity


       