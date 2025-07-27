import pandas as pd
import xml.etree.ElementTree as ET

def process_fcd(input_file):
    tree = ET.parse(input_file)
    data = []
    for timestep in tree.getroot():
        time = float(timestep.attrib['time'])
        for vehicle in timestep:
            data.append({
                'time': time,
                'id': vehicle.attrib['id'],
                'x': float(vehicle.attrib['x']),
                'y': float(vehicle.attrib['y']),
                'speed': float(vehicle.attrib['speed']),
                'type': vehicle.attrib.get('type', 'passenger')
            })
    return pd.DataFrame(data)

urban_df = process_fcd('../output/urban_traffic.xml')
suburban_df = process_fcd('../output/suburban_traffic.xml')

urban_df.to_csv('../output/urban_traffic.csv', index=False)
suburban_df.to_csv('../output/suburban_traffic.csv', index=False)