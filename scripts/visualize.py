import pandas as pd
import matplotlib.pyplot as plt

urban = pd.read_csv('../output/urban_traffic.csv')
suburban = pd.read_csv('../output/suburban_traffic.csv')

# Speed distribution comparison
plt.figure(figsize=(10,5))
plt.hist(urban['speed'], bins=30, alpha=0.5, label='Urban')
plt.hist(suburban['speed'], bins=30, alpha=0.5, label='Suburban')
plt.xlabel('Speed (m/s)')
plt.ylabel('Frequency')
plt.legend()
plt.savefig('../output/speed_comparison.png')