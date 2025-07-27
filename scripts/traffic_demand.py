import os
import subprocess
from pathlib import Path

# Convert to absolute paths
BASE_DIR = Path(__file__).parent.parent
SUMO_HOME = "C:/Program Files (x86)/Eclipse/Sumo"

NET_FILES = {
    "urban": str(BASE_DIR / "urban" / "urban.net.xml"),
    "suburban": str(BASE_DIR / "suburban" / "suburban.net.xml")
}

OUTPUT_DIRS = {
    "urban": str(BASE_DIR / "urban"),
    "suburban": str(BASE_DIR / "suburban")
}

def generate_demand(area):
    print(f"Generating {area} demand...")
    
    # Morning peak (7-9 AM)
    subprocess.run([
       "python", os.path.join(SUMO_HOME, "tools", "randomTrips.py"),
       "-n", NET_FILES[area],
       "-b", "25200", "-e", "32400", "-p", "0.8",
       "--prefix", "morning_",  # ← Add this line
       "-o", os.path.join(OUTPUT_DIRS[area], "morning_peak.trips.xml")
    ])

    # Evening peak (5-7 PM)
    subprocess.run([
       "python", os.path.join(SUMO_HOME, "tools", "randomTrips.py"),
       "-n", NET_FILES[area],
       "-b", "61200", "-e", "68400", "-p", "1.0",
       "--prefix", "evening_",  # ← Add this line
       "-o", os.path.join(OUTPUT_DIRS[area], "evening_peak.trips.xml")
    ])

    print(f"Successfully created demand files in {OUTPUT_DIRS[area]}")

if __name__ == "__main__":
    generate_demand("urban")
    generate_demand("suburban")