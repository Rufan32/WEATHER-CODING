# Data Description

The project uses simulated meteorological data that follows seasonal patterns:
- Temperature: Base value of 20°C with ±5°C sinusoidal variation
- Humidity: Base value of 60% with ±15% sinusoidal variation
- Wind speed: Base value of 5m/s with ±3m/s sinusoidal variation

# Visualization Description

- **Colors**: From blue (cold) to red (hot) representing temperature changes
- **Wave frequency**: Proportional to temperature
- **Wave amplitude**: Proportional to humidity
- **Wave complexity**: Proportional to wind speed

# Output

The program will:
1. Display a real-time animation window
2. Attempt to save the animation as an MP4 file (requires ffmpeg)
3. If MP4 saving fails, attempt to save as GIF (requires pillow)

# Customization Options

You can modify the following parts to customize the visualization:
- `cmap` variable: Change the color scheme
- `generate_waveform` method: Change the waveform generation algorithm
- `generate_sample_data` method: Modify the data generation logic

# Technology Stack

- Python 3
- Matplotlib (for visualization)
- NumPy (for numerical computation)
- Pandas (for data processing)

# Extension Suggestions

1. Connect to real APIs to obtain live meteorological data
2. Add more meteorological parameters (such as atmospheric pressure, precipitation)
3. Create interactive controls to adjust visualization parameters
4. Add audio elements to create data sonification effects