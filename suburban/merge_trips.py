import xml.etree.ElementTree as ET

# Parse input files
morning = ET.parse('suburban_morning.trips.xml')
evening = ET.parse('suburban_evening.trips.xml')

# Create new root
merged = ET.Element('routes')

# Add all vehicles
for vehicle in morning.findall('vehicle') + evening.findall('vehicle'):
    merged.append(vehicle)

# Save output
ET.ElementTree(merged).write('suburban.trips.xml')