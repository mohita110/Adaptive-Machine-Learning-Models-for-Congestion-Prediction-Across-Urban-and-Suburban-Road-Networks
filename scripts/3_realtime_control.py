from model_definitions import HybridCongestionPredictor
from joblib import load
import traci
import pandas as pd
import os
from datetime import datetime
import time

def run_simulation(sumocfg_path, model_path, area_type, max_steps=200):
    try:
        # Load the trained model
        predictor = load(model_path)
        
        # Start SUMO with auto-quit and longer delay
        traci.start([
            "sumo-gui", 
            "-c", os.path.abspath(sumocfg_path),
            "--quit-on-end",
            "--delay", "100"  # Slower visualization
        ])
        
        print(f"Running real-time control for {'urban' if area_type else 'suburban'} area")
        print(f"Target simulation steps: {max_steps}")
        
        # Get all available traffic lights
        tl_ids = traci.trafficlight.getIDList()
        print(f"Detected traffic lights: {tl_ids}")
        
        step = 0
        while step < max_steps:
            try:
                traci.simulationStep()
                current_time = traci.simulation.getTime()
                
                # Collect data from all edges
                for edge in traci.edge.getIDList():
                    vehicles = traci.edge.getLastStepVehicleNumber(edge)
                    if vehicles > 0:
                        # Prepare prediction input
                        current_state = pd.DataFrame([{
                            'vehicle_count': vehicles,
                            'avg_speed_kmh': traci.edge.getLastStepMeanSpeed(edge) * 3.6,
                            'area_type': area_type,
                            'hour': datetime.now().hour,
                            'is_peak': int(datetime.now().hour in [7,8,9,17,18,19])
                        }])
                        
                        # Predict congestion
                        predicted_wait = predictor.predict(current_state)[0]
                        
                        # Urban area controls
                        if area_type and predicted_wait > 25:
                            if tl_ids:
                                try:
                                    tl_id = tl_ids[0]  # Use first traffic light
                                    program = traci.trafficlight.getAllProgramLogics(tl_id)[0]
                                    phases = program.getPhases()
                                    current_phase = traci.trafficlight.getPhase(tl_id)
                                    next_phase = (current_phase + 1) % len(phases)
                                    traci.trafficlight.setPhase(tl_id, next_phase)
                                except Exception as e:
                                    print(f"Traffic light error: {e}")
                                    # Fallback to speed adjustment
                                    traci.edge.setMaxSpeed(edge, max(30, traci.edge.getMaxSpeed(edge) - 5))
                            else:
                                # Speed adjustment if no traffic lights
                                traci.edge.setMaxSpeed(edge, max(30, traci.edge.getMaxSpeed(edge) - 5))
                        
                        # Suburban area controls
                        elif not area_type and predicted_wait > 15:
                            traci.edge.setMaxSpeed(edge, max(30, traci.edge.getMaxSpeed(edge) - 5))
                
                # Progress reporting
                step += 1
                if step % 20 == 0:
                    print(f"Completed {step}/{max_steps} steps | Sim time: {current_time:.1f}s")
                    
            except traci.exceptions.TraCIException as e:
                if "connection closed" in str(e):
                    print("SUMO disconnected - reconnecting...")
                    traci.close()
                    time.sleep(1)
                    traci.start([
                        "sumo-gui", 
                        "-c", os.path.abspath(sumocfg_path),
                        "--quit-on-end"
                    ])
                    continue
                raise
                
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        traci.close()
        print("Simulation completed")

if __name__ == "__main__":
    run_simulation(
        sumocfg_path="../urban/urban.sumocfg",
        model_path="../models/hybrid_predictor.joblib",
        area_type=1  # 1=urban, 0=suburban
    )