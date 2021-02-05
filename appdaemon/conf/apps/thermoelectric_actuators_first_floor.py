import appdaemon.plugins.hass.hassapi as hass
# Import the PCA9685 module.
import pca9685
import time

class ThermoelectricActuatorsFirstFloor(hass.Hass):

    def initialize(self):
        self.listen_state(self.trigger, "input_number.thermo_actuator_bathroom")
        self.listen_state(self.trigger, "input_number.thermo_actuator_bathroom_ladder")
        self.listen_state(self.trigger, "input_number.thermo_actuator_living_and_diving_room")
        self.listen_state(self.trigger, "input_number.thermo_actuator_workroom")
        self.listen_state(self.trigger, "input_number.thermo_actuator_kitchen")
        self.listen_state(self.trigger, "input_number.thermo_actuator_corridor_and_toilet")
        self.listen_state(self.trigger, "input_number.thermo_actuator_north_room")
        self.listen_state(self.trigger, "input_number.thermo_actuator_parents_bedroom_window")
        self.listen_state(self.trigger, "input_number.thermo_actuator_parents_bedroom_door")
        self.listen_state(self.trigger, "input_number.thermo_actuator_middle_room")
        self.listen_state(self.trigger, "input_number.thermo_actuator_corner_room")
        self.listen_state(self.trigger, "input_number.thermo_actuator_thomas_bedroom")

    def trigger(self, entity, attribute, old, new, kwargs):    

        # Initialise the PCA9685 using the default address (0x40).
        PCA9685_ADDRESS_FIRST_FLOOR = 0x40
        pwm = pca9685.PCA9685(PCA9685_ADDRESS_FIRST_FLOOR)

        # Frequency in Hertz
        PWM_FREQUENCY = 100 
        pwm.set_pwm_freq(PWM_FREQUENCY)
       
        # Order in this array is the same as order actuators in distributor (0 is left, 11 is right)
        pwm_percent = []

        # 0 actuator (bathroom)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_bathroom"))
        # 1 actuator (batroom ladder)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_bathroom_ladder"))
        # 2 actuator (living room and diving room)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_living_and_diving_room"))
        # 3 actuator (workroom)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_workroom"))
        # 4 actuator (kitcher)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_kitchen"))
        # 5 actuator (corridor and toiler)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_corridor_and_toilet"))
        # 6 actuator (north room)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_north_room"))
        # 7 actuator (parents bedroom - window)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_parents_bedroom_window"))
        # 8 actuator (parents bedrrom - window)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_parents_bedroom_door"))
        # 9 actuator (middle room)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_middle_room"))
        # 10 actuator (corner room)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_corner_room"))
        # 11 actuator (thomas bedroom)
        pwm_percent.append(self.get_state("input_number.thermo_actuator_thomas_bedroom"))
        
        # Sets all channels
        for index in range(len(pwm_percent)):
            pwm.set_pwm(index, 0, self.get_pwm_pulse(pwm_percent[index]))

        time.sleep(1)

        # Checks all channels are correct (pwm pulse), otherwise sets again
        state = "true"
        while state == "true":
            state = "false"
            for index in range(len(pwm_percent)):
                if self.get_pwm_pulse(pwm_percent[index]) != pwm.get_pwm(index):
                    pwm_pulse = self.get_pwm_pulse(pwm_percent[index])
                    pwm.set_pwm(index, 0, pwm_pulse)
                    state = "true"

    def get_pwm_pulse(self, pwm_percent):
        # Convert to float number
        pwm_value = float(pwm_percent)/100.0
        # Gets pwm pulse
        pwm_pulse = round(4095 * pwm_value) 

        return int(pwm_pulse)