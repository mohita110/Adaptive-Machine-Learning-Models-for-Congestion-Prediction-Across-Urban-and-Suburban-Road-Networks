import traci
import pandas as pd

WEATHER_CONDITIONS = {
    "clear": {"speed_factor": 1.0, "friction": 1.0},
    "rain": {"speed_factor": 0.8, "friction": 0.7},
    "fog": {"speed_factor": 0.6, "friction": 0.9}
}

def simulate_with_weather(sumocfg_path, output_prefix):
    traci.start(["sumo", "-c", sumocfg_path])
    data = []
    
    while traci.simulation.getMinExpectedNumber() > 0:
        current_time = traci.simulation.getTime()
        weather = get_weather_condition(current_time)
        apply_weather(weather)
        
        for edge in traci.edge.getIDList():
            data.append({
                "time": current_time,
                "edge": edge,
                "speed": traci.edge.getLastStepMeanSpeed(edge),
                "vehicles": traci.edge.getLastStepVehicleNumber(edge),
                "weather": weather,
                "is_peak": is_peak_hour(current_time)
            })
        traci.simulationStep()
    
    pd.DataFrame(data).to_csv(f"output/{output_prefix}.csv", index=False)
    traci.close()

def is_peak_hour(time):
    return (25200 <= time <= 32400) or (61200 <= time <= 68400)  # 7-9AM, 5-7PM