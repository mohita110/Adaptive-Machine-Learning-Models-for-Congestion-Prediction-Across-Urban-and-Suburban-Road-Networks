import traci
import pandas as pd
from pathlib import Path

class CongestionDetector:
    # Add to CongestionDetector class
    def __init__(self, output_dir="../output"):
        self.weather_impact = {
            "clear": 1.0,
            "rain": 0.85, 
            "fog": 0.7,
            "storm": 0.5
        }
    # ... rest of init ...

    def detect(self):
        current_weather = traci.simulation.getParameter("weather")
        weather_factor = self.weather_impact.get(current_weather, 1.0)
    
        for edge in traci.edge.getIDList():
            max_speed = traci.edge.getMaxSpeed(edge) * weather_factor
            # Rest of detection logic...
    def __init__(self, output_dir="../output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.congestion_data = []
        
    def detect(self):
        """Main detection loop"""
        for edge in traci.edge.getIDList():
            current_speed = traci.edge.getLastStepMeanSpeed(edge)
            max_speed = traci.edge.getMaxSpeed(edge)
            vehicles = traci.edge.getLastStepVehicleNumber(edge)
            
            # Congestion threshold (40% speed reduction)
            if current_speed < 0.6 * max_speed and vehicles > 3:
                self._record_congestion(
                    edge=edge,
                    time=traci.simulation.getTime(),
                    speed=current_speed,
                    vehicles=vehicles,
                    max_speed=max_speed
                )
    
    def _record_congestion(self, **data):
        """Store congestion events with timestamps"""
        self.congestion_data.append(data)
        
    def save_results(self, area_type):
        """Save to CSV with area classification"""
        df = pd.DataFrame(self.congestion_data)
        df['area_type'] = area_type  # 'urban' or 'suburban'
        output_path = self.output_dir / f"congestion_{area_type}.csv"
        df.to_csv(output_path, index=False)
        print(f"Saved congestion data to {output_path}")

def run_detection(sumocfg_path, area_type):
    """Initialize and run detection"""
    traci.start(["sumo", "-c", sumocfg_path])
    detector = CongestionDetector()
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        detector.detect()
    
    detector.save_results(area_type)
    traci.close()

if __name__ == "__main__":
    # Example usage (modify paths as needed)
    run_detection(
        sumocfg_path="../urban/urban.sumocfg",
        area_type="urban"
    )