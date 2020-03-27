import appdaemon.plugins.hass.hassapi as hass
import i2c_lcd_driver

class I2CLCD(hass.Hass):

  def initialize(self):
    self.listen_state(self.trigger, "sensor.hot_water_tank_top_temperature")
    self.listen_state(self.trigger, "sensor.hot_water_tank_middle_temperature")
    self.listen_state(self.trigger, "input_boolean.manual_control_devices")

  def trigger(self, entity, attribute, old, new, kwargs):
    first_floor_lcd = i2c_lcd_driver.lcd(0x26)
    degree = [      
        [ 0b00111,
	      0b00101,
	      0b00111,
	      0b00000,
	      0b00000,
	      0b00000,
	      0b00000,
	      0b00000
          ],]
    first_floor_lcd.lcd_load_custom_chars(degree)
 
    hot_water_tank_top_temperature = self.get_state("sensor.hot_water_tank_top_temperature")
    hot_water_tank_middle_temperature = self.get_state("sensor.hot_water_tank_middle_temperature")
    
    first_floor_lcd.lcd_display_string("Cidlo 1: "+ hot_water_tank_top_temperature + " " + chr(0) + "C", 1)
    first_floor_lcd.lcd_display_string("Cidlo 2: "+ hot_water_tank_middle_temperature + " " + chr(0) + "C", 2)
   