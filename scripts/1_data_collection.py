import traci
import pandas as pd
import os
import random
from datetime import datetime, timedelta

def collect_data(sumocfg_path, output_path, max_steps=300, sample_rate=0.3):
    try:
        traci.start(["sumo", "-c", os.path.abspath(sumocfg_path)])
        print(f"Collecting data from {os.path.basename(sumocfg_path)}...")
        
        data = []
        current_time = datetime.now().replace(hour=7, minute=0, second=0)
        
        for step in range(max_steps):
            traci.simulationStep()
            
            # Only sample 30% of edges to reduce data volume
            if random.random() < sample_rate:
                for edge in traci.edge.getIDList():
                    vehicles = traci.edge.getLastStepVehicleNumber(edge)
                    if vehicles > 0:  # Only record edges with vehicles
                        waiting_time = traci.edge.getWaitingTime(edge)
                        speed = traci.edge.getLastStepMeanSpeed(edge)
                        
                        data.append({
                            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "edge_id": edge,
                            "vehicle_count": vehicles,
                            "avg_speed_kmh": speed * 3.6,  # Convert m/s to km/h
                            "waiting_time_sec": waiting_time,
                            "congestion_level": min(int(waiting_time / 10), 5)  # 0-5 scale
                        })
            
            current_time += timedelta(seconds=1)
            if step % 50 == 0:
                print(f"Step {step}/{max_steps} - Collected {len(data)} records")
        
        # Ensure we have exactly 3000 records per area
        df = pd.DataFrame(data[-3000:]) if len(data) > 3000 else pd.DataFrame(data)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} records to {output_path}")
        
    finally:
        traci.close()

# Collect data for both areas
collect_data("../urban/urban.sumocfg", "../output/urban_traffic.csv")
collect_data("../suburban/suburban.sumocfg", "../output/suburban_traffic.csv")