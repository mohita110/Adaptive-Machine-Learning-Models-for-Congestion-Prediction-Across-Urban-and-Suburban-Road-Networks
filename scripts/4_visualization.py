import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import numpy as np

# Updated style configuration for modern matplotlib/seaborn
sns.set_theme(style="whitegrid")  # This replaces plt.style.use('seaborn')
sns.set_palette("husl")

OUTPUT_DIR = "../output/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_and_prepare_data():
    """Load and merge urban/suburban data with proper labeling"""
    try:
        urban = pd.read_csv("../output/urban_traffic.csv")
        suburban = pd.read_csv("../output/suburban_traffic.csv")
        
        urban['area_type'] = 'Urban'
        suburban['area_type'] = 'Suburban'
        
        combined = pd.concat([urban, suburban])
        combined['timestamp'] = pd.to_datetime(combined['timestamp'])
        combined['hour'] = combined['timestamp'].dt.hour
        combined['minute'] = combined['timestamp'].dt.minute
        
        # Calculate congestion levels
        combined['congestion'] = pd.cut(combined['waiting_time_sec'],
                                       bins=[0, 10, 20, 30, 45, 60, np.inf],
                                       labels=['0-10', '10-20', '20-30', '30-45', '45-60', '60+'])
        
        return combined
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

def plot_waiting_time_distribution(data):
    """Plot distribution of waiting times"""
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='area_type', y='waiting_time_sec', data=data)
    plt.title('Vehicle Waiting Time Distribution')
    plt.xlabel('Area Type')
    plt.ylabel('Waiting Time (seconds)')
    plt.savefig(f"{OUTPUT_DIR}/waiting_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_congestion_by_hour(data):
    """Plot congestion patterns throughout the day"""
    plt.figure(figsize=(14, 7))
    
    hourly = data.groupby(['area_type', 'hour'])['waiting_time_sec'].mean().reset_index()
    
    sns.lineplot(x='hour', y='waiting_time_sec', hue='area_type', 
                 data=hourly, marker='o', linewidth=2.5)
    
    plt.title('Average Waiting Time by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Waiting Time (seconds)')
    plt.xticks(range(24))
    plt.grid(True, alpha=0.3)
    plt.legend(title='Area Type')
    plt.savefig(f"{OUTPUT_DIR}/congestion_by_hour.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_top_congested_edges(data, top_n=5):
    """Plot most congested edges in each area"""
    plt.figure(figsize=(14, 8))
    
    top_urban = data[data['area_type'] == 'Urban'].groupby('edge_id')['waiting_time_sec'] \
        .mean().nlargest(top_n).reset_index()
    top_suburban = data[data['area_type'] == 'Suburban'].groupby('edge_id')['waiting_time_sec'] \
        .mean().nlargest(top_n).reset_index()
    
    plt.subplot(2, 1, 1)
    sns.barplot(x='edge_id', y='waiting_time_sec', data=top_urban)
    plt.title(f'Top {top_n} Congested Urban Edges')
    plt.xlabel('Edge ID')
    plt.ylabel('Avg Waiting Time (sec)')
    
    plt.subplot(2, 1, 2)
    sns.barplot(x='edge_id', y='waiting_time_sec', data=top_suburban)
    plt.title(f'Top {top_n} Congested Suburban Edges')
    plt.xlabel('Edge ID')
    plt.ylabel('Avg Waiting Time (sec)')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_congested_edges.png", dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("Loading and preparing data...")
    data = load_and_prepare_data()
    
    print("Generating visualizations...")
    plot_waiting_time_distribution(data)
    plot_congestion_by_hour(data)
    plot_top_congested_edges(data)
    
    print(f"Visualizations saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()