import traci
import random

WEATHER_TYPES = ["clear", "rain", "fog", "storm"]

def set_weather(condition):
    traci.simulation.setParameter("weather", condition)
    # Adjust vehicle behavior
    if condition == "rain":
        traci.vehicletype.setSpeedFactor("passenger", 0.8)
    elif condition == "fog":
        traci.vehicletype.setMaxSpeed("passenger", 15)  # km/h

def random_weather_change():
    if traci.simulation.getTime() % 3600 == 0:  # Every hour
        set_weather(random.choice(WEATHER_TYPES))