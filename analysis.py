import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("last_mile_delivery_dataset.csv")
print(df.shape)

# Convert time column
df['order_time'] = pd.to_datetime(df['order_time'])

# Extract hour
df['hour'] = df['order_time'].dt.hour

# Create Peak / Off-Peak category
df['peak_hour'] = np.where(
    ((df['hour'] >= 8) & (df['hour'] < 10)) |
    ((df['hour'] >= 17) & (df['hour'] < 20)),
    'Peak',
    'Off-Peak'
)

# Average delay comparison
result = df.groupby('peak_hour')['delay_mins'].mean()

print("Average Delay (mins)")
print(result)

# Quantify difference
difference = result['Peak'] - result['Off-Peak']

print("\nDifference =", round(difference, 2), "minutes")

# Visualization
result.plot(kind='bar')

plt.title("Peak vs Off-Peak Average Delay")
plt.xlabel("Time Category")
plt.ylabel("Average Delay (mins)")
plt.show()


print("\nDifference :",round(difference,2),"minutes")

#question2

# Median delay by weather condition
weather_delay = df.groupby('weather_condition')['delay_mins'].median()

print(weather_delay)

weather_delay.plot(kind='bar')
plt.title("Weather vs Delay")
plt.ylabel("Median Delay")
plt.show()

# Orders during rain
rain = df[df['weather_condition'] == 'Rain']

# Rain impact by order type
rain_effect = rain.groupby('order_type')['delay_mins'].median()

print(rain_effect)

rain_effect.plot(kind='bar')
plt.title("Rain Impact by Order Type")
plt.ylabel("Median Delay")
plt.show()

# Most affected order type
print("\nOrder type hit hardest by rain:", rain_effect.idxmax())


#q3

new_riders = df[df['rider_experience_yrs'] < 2]['delay_mins']

experienced = df[df['rider_experience_yrs'] > 4]['delay_mins']

print("New Riders Avg Delay:",
      round(new_riders.mean(), 2))

print("Experienced Riders Avg Delay:",
      round(experienced.mean(), 2))

#q4


df['on_time'] = np.where(df['delay_mins'] <= 0, 1, 0)

city = df.groupby('city')['on_time'].mean() * 100

df['month'] = pd.to_datetime(df['order_date']).dt.month

monthly = df.groupby('month')['delay_mins'].mean()

vehicle = df.groupby('vehicle_type')['delay_mins'].mean()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

city.plot(kind='bar', ax=axes[0])
axes[0].set_title('City-wise On-Time Rate (%)')

monthly.plot(marker='o', ax=axes[1])
axes[1].set_title('Monthly Delay Trend')

vehicle.plot(kind='bar', ax=axes[2])
axes[2].set_title('Vehicle Type Comparison')

plt.tight_layout()
plt.show()