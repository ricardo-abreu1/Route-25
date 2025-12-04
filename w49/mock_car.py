import logging

# Configure logging
logging.basicConfig(
    filename='car_events.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

        # Internal state
        self.speed = 0
        self.lights = False
        self.clutch = False
        self.radio = False
        self.blinkers = None  # "left", "right", or None
        self.reverse_light = False
        self.hazard_lights = False
        self.wipers = "Off"  # "slow", "medium", "fast"

    def log_action(self, action_name):
        logging.info(f"{action_name} | State: "
                     f"Car Brand={self.brand}, Model={self.model}, Year={self.year}, "
                     f"Speed={self.speed}, Lights={self.lights}, Clutch={self.clutch}, "
                     f"Radio={self.radio}, Blinkers={self.blinkers}, Reverse={self.reverse_light}, "
                     f"Hazard={self.hazard_lights}, Wipers={self.wipers}")

    def details(self):
        return f"Car Details: {self.brand} {self.model} {self.year}"

    def accelerate(self):
        self.speed += 10
        self.log_action("Accelerate")
        return f"Currently accelerating... Speed at {self.speed} km/h"

    def brake(self):
        self.speed = max(0, self.speed - 10)
        self.log_action("Brake")
        return f"Currently braking... Speed at {self.speed} km/h"

    def lights_on(self):
        self.lights = True
        self.log_action("Lights ON")
        return "Lights turned ON."

    def lights_off(self):
        self.lights = False
        self.log_action("Lights OFF")
        return "Lights turned OFF."

    def clutch_press(self):
        self.clutch = True
        self.log_action("Clutch Pressed")
        return "Clutch was pressed."

    def clutch_release(self):
        self.clutch = False
        self.log_action("Clutch Released")
        return "Clutch released."

    def radio_on(self):
        self.radio = True
        self.log_action("Radio ON")
        return "Radio turned ON."

    def radio_off(self):
        self.radio = False
        self.log_action("Radio OFF")
        return "Radio turned OFF."

    def blinkers_left(self):
        self.blinkers = "left"
        self.log_action("Blinkers LEFT")
        return "Left blinkers ON."

    def blinkers_right(self):
        self.blinkers = "right"
        self.log_action("Blinkers RIGHT")
        return "Right blinkers ON."

    def reverse_light_on(self):
        self.reverse_light = True
        self.log_action("Reverse Light ON")
        return "Reverse light ON."

    def reverse_light_off(self):
        self.reverse_light = False
        self.log_action("Reverse Light OFF")
        return "Reverse light OFF."

    def hazard_lights_on(self):
        self.hazard_lights = True
        self.log_action("Hazard Lights ON")
        return "Hazard lights ON."

    def hazard_lights_off(self):
        self.hazard_lights = False
        self.log_action("Hazard Lights OFF")
        return "Hazard lights OFF."

    def wipers_light(self):
        self.wipers = "slow"
        self.log_action("Wipers Slow")
        return "Wipers speed: Slow"

    def wipers_medium(self):
        self.wipers = "medium"
        self.log_action("Wipers Medium")
        return "Wipers speed: Medium."

    def wipers_fast(self):
        self.wipers = "fast"
        self.log_action("Wipers Fast")
        return "Wipers speed: Fast."
