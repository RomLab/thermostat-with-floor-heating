import appdaemon.plugins.hass.hassapi as hass
import i2c_lcd_driver

class I2CLCD(hass.Hass):

  def initialize(self):
    self.listen_state(self.trigger, "sensor.hot_water_tank_middle")
    self.listen_state(self.trigger, "sensor.hot_water_tank_bottom")
    self.listen_state(self.trigger, "switch.blue_led")

  def trigger(self, entity, attribute, old, new, kwargs): 
    state_switch = None
    if(entity == "switch.blue_led"):
      state_switch = self.get_state("switch.blue_led")

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
    cellar_lcd = i2c_lcd_driver.lcd(0x25)
    first_floor_lcd= i2c_lcd_driver.lcd(0x27)  
    second_floor_lcd= i2c_lcd_driver.lcd(0x26)

    hot_water_tank_top_temperature = self.get_state("sensor.hot_water_tank_top")
    hot_water_tank_middle_temperature = self.get_state("sensor.hot_water_tank_middle")
    hot_water_tank_bottom_temperature = self.get_state("sensor.hot_water_tank_bottom")
    # Notification about flooding in a fireplace
    if(state_switch == "on"):  
      cellar_lcd.lcd_display_string("  Zatop v krbu!", 1)
      cellar_lcd.lcd_display_string("Cidlo 3: " + hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)

      first_floor_lcd.lcd_display_string("  Zatop v krbu!", 1)
      first_floor_lcd.lcd_display_string("Cidlo 3: " + hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)

      second_floor_lcd.lcd_display_string("  Zatop v krbu!", 1)
      second_floor_lcd.lcd_display_string("Cidlo 3: " + hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)
    else:
      first_floor_lcd.lcd_load_custom_chars(degree)
      second_floor_lcd.lcd_load_custom_chars(degree)
      cellar_lcd.lcd_load_custom_chars(degree)
  
      

      cellar_lcd.lcd_display_string("Cidlo 2: " + hot_water_tank_middle_temperature + " " + chr(0) + "C", 1)
      cellar_lcd.lcd_display_string("Cidlo 3: " + hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)

      first_floor_lcd.lcd_display_string("Cidlo 2: " + hot_water_tank_middle_temperature + " " + chr(0) + "C", 1)
      first_floor_lcd.lcd_display_string("Cidlo 3: " + hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)

      second_floor_lcd.lcd_display_string("Cidlo 2: " + hot_water_tank_middle_temperature + " " + chr(0) + "C", 1)
      second_floor_lcd.lcd_display_string("Cidlo 3: " + hot_water_tank_bottom_temperature + " " + chr(0) + "C", 2)

      


   