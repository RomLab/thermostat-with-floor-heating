import appdaemon.plugins.hass.hassapi as hass
import i2c_lcd_driver

class I2CLCD(hass.Hass):

  def initialize(self):
    self.listen_state(self.trigger, "sensor.hot_water_tank_middle")
    self.listen_state(self.trigger, "sensor.hot_water_tank_bottom")

  def trigger(self, entity, attribute, old, new, kwargs):    
    first_floor_lcd = i2c_lcd_driver.lcd(0x26)
    second_floor_lcd = i2c_lcd_driver.lcd(0x27)
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
    second_floor_lcd.lcd_load_custom_chars(degree)
 
    hot_water_tank_middle_temperature = self.get_state("sensor.hot_water_tank_middle")
    hot_water_tank_bottom_temperature = self.get_state("sensor.hot_water_tank_bottom")
    
    first_floor_lcd.lcd_display_string("Cidlo 2: "+ hot_water_tank_middle_temperature + " " + chr(0) + "C", 1)
    first_floor_lcd.lcd_display_string("Cidlo 3: "+ hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)

    second_floor_lcd.lcd_display_string("Cidlo 2: "+ hot_water_tank_middle_temperature + " " + chr(0) + "C", 1)
    second_floor_lcd.lcd_display_string("Cidlo 3: "+ hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)
   