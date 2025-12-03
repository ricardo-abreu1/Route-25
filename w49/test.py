from mock_car import Car

# Create a car instance
my_car = Car("Renault", "Clio", 2025)

# Test actions
print(my_car.details())
print(my_car.accelerate())
print(my_car.accelerate())
print(my_car.brake())
print(my_car.lights_on())
print(my_car.clutch_press())
print(my_car.radio_on())
print(my_car.blinkers_left())
print(my_car.reverse_light_on())
print(my_car.hazard_lights_on())
print(my_car.wipers_fast())

# Show final state
print("\nFinal State:")
print(f"Speed: {my_car.speed}")
print(f"Lights: {my_car.lights}")
print(f"Clutch: {my_car.clutch}")
print(f"Radio: {my_car.radio}")
print(f"Blinkers: {my_car.blinkers}")
print(f"Reverse Light: {my_car.reverse_light}")
print(f"Hazard Lights: {my_car.hazard_lights}")
print(f"Wipers: {my_car.wipers}")
