import pandas as pd
import seaborn as sns

def analyze():
    df = pd.read_csv("output/congestion_suburban.csv")
    weather_df = pd.read_csv("output/weather_log.csv")  # From your weather controller
    
    merged = pd.merge(df, weather_df, on="time")
    
    # Group by weather condition
    results = merged.groupby('weather').agg({
        'speed': 'mean',
        'vehicles': 'sum'
    })
    
    print("Weather Impact Analysis:")
    print(results)
    
    # Visualize
    sns.boxplot(x='weather', y='speed', data=merged)
    plt.savefig("output/weather_impact.png")

analyze()