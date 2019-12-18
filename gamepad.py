#!/usr/bin/python3

import asyncio

from evdev import InputDevice, ecodes, ff, list_devices


class gamepad():
    def __init__(self, file = '/dev/input/event3'):
        #self.event_value = 0
        self.power_on = True
        self.device_file = InputDevice(file)
        self.joystick_left_y_flag = False
        self.joystick_left_x_flag = False
        self.joystick_right_y_flag = False
        self.joystick_right_x_flag = False
        self.joystick_left_y = 0 # values are mapped to [-1 ... 1]
        self.joystick_left_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_y = 0 # values are mapped to [-1 ... 1]
        self.trigger_right = 0 # values are mapped to [0 ... 1]
        self.trigger_left = 0 # values are mapped to [0 ... 1]
        self.button_x = False
        self.button_y = False
        self.button_b = False
        self.button_a = False
        self.dpad_up_down = 0
        self.dpad_left_right = 0
        self.dpad = None
        self.bump_left = False
        self.bump_right = False
        self.button_menu = False
        self.button_view = False
        self.rumble_effect = 0
        self.effect1_id = 0 # light rumble, played continuously
        self.effect2_id = 0 # strong rumble, played once
        self.load_effects()

    def load_effects(self):
        #effect 1, light rumble
        rumble = ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0x500)
        duration_ms = 300
        effect = ff.Effect(ecodes.FF_RUMBLE, -1, 0, ff.Trigger(0, 0), ff.Replay(duration_ms, 0), ff.EffectType(ff_rumble_effect=rumble))
        self.effect1_id = self.device_file.upload_effect(effect)
        # effect 2, strong rumble
        rumble = ff.Rumble(strong_magnitude=0xc000, weak_magnitude=0x0000)
        duration_ms = 200
        effect = ff.Effect(ecodes.FF_RUMBLE, -1, 0, ff.Trigger(0, 0), ff.Replay(duration_ms, 0), ff.EffectType(ff_rumble_effect=rumble))
        self.effect2_id = self.device_file.upload_effect(effect)


    async def read_gamepad_input(self): # asyncronus read-out of events
        max_abs_joystick_left_x = 0xFFFF/2
        uncertainty_joystick_left_x = 2500
        max_abs_joystick_left_y = 0xFFFF/2
        uncertainty_joystick_left_y = 2500
        max_abs_joystick_right_x = 0xFFFF/2
        uncertainty_joystick_right_x = 2000
        max_abs_joystick_right_y = 0xFFFF/2
        uncertainty_joystick_right_y = 2000
        max_trigger = 1023

        async for event in self.device_file.async_read_loop():
            if not(self.power_on): #stop reading device when power_on = false
                    break

            #print(str(event.type) + ' ' + str(event.code) + ' ' + str(event.value))

            if event.type == 3: # type is analog trigger or joystick
                if event.code == 1: # left joystick y-axis
                    self.joystick_left_y_flag = True
                    if -event.value > uncertainty_joystick_left_y:
                        self.joystick_left_y = (-event.value - uncertainty_joystick_left_y) / (max_abs_joystick_left_y - uncertainty_joystick_left_y + 1)
                    elif -event.value < -uncertainty_joystick_left_y:
                        self.joystick_left_y = (-event.value + uncertainty_joystick_left_y) / (max_abs_joystick_left_y - uncertainty_joystick_left_y + 1)
                    else:
                        self.joystick_left_y = 0
                elif event.code == 0: # left joystick x-axis
                    self.joystick_left_x_flag = True
                    if event.value > uncertainty_joystick_left_x:
                        self.joystick_left_x = (event.value - uncertainty_joystick_left_x) / (max_abs_joystick_left_x - uncertainty_joystick_left_x + 1)
                    elif event.value < -uncertainty_joystick_left_x:
                        self.joystick_left_x = (event.value + uncertainty_joystick_left_x) / (max_abs_joystick_left_x - uncertainty_joystick_left_x + 1)
                    else:
                        self.joystick_left_x = 0
                elif event.code == 3: # right joystick x-axis
                    self.joystick_right_x_flag = True
                    if event.value > uncertainty_joystick_right_x:
                        self.joystick_right_x = (event.value - uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                    elif event.value < -uncertainty_joystick_right_x:
                        self.joystick_right_x = (event.value + uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                    else:
                        self.joystick_right_x = 0
                elif event.code == 4: # right joystick y-axis
                    self.joystick_right_y_flag = True
                    if -event.value > uncertainty_joystick_right_y:
                        self.joystick_right_y = (-event.value - uncertainty_joystick_right_y) / (max_abs_joystick_right_y - uncertainty_joystick_right_y + 1)
                    elif -event.value < -uncertainty_joystick_right_y:
                        self.joystick_right_y = (-event.value + uncertainty_joystick_right_y) / (max_abs_joystick_right_y - uncertainty_joystick_right_y + 1)
                    else:
                        self.joystick_right_y = 0
                elif event.code == 5: # right trigger
                    self.trigger_right = event.value / max_trigger
                elif event.code == 2: # left trigger
                    self.trigger_left = event.value / max_trigger
                elif event.code == 16: # dpad left/right
                    self.dpad = True
                    self.dpad_left_right = event.value
                elif event.code == 17: # dpad up/down
                    self.dpad = True
                    self.dpad_up_down = event.value

            if event.type == 1: # type is button
                if event.code == 304: # button "A" pressed ?
                    self.button_a = True
                if event.code == 307: # button "X" pressed ?
                    self.button_x = True
                if event.code == 308: # button "Y" pressed ?
                    self.button_y = True
                if event.code == 305: # button "B" pressed ?
                    self.button_b = True
                if event.code == 315: # button "Menu" pressed ?
                    self.button_menu = True if event.value == 1 else False
                if event.code == 314: # button "View" pressed ?
                    self.button_view = True if event.value == 1 else False
                if event.code == 311: # bumper "right" pressed ?
                    self.bump_right = True if event.value == 1 else False
                if event.code == 310: # bumper "left" pressed ?
                    self.bump_left = True if event.value == 1 else False


    async def rumble(self): # asyncronus control of force feed back effects
        repeat_count = 1
        while self.power_on:
            if self.rumble_effect == 1:
                self.device_file.write(ecodes.EV_FF, self.effect1_id, repeat_count)
            elif self.rumble_effect == 2:
                self.device_file.write(ecodes.EV_FF, self.effect2_id, repeat_count)
                self.rumble_effect = 0 # turn of effect in order to play effect2 only once
            await asyncio.sleep(0.2)

    def erase_rumble(self):
        self.device_file.erase_effect(self.effect1_id)
