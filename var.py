import pandas as pd
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt

# Load the simulated dataset into a pandas DataFrame
data = pd.read_csv('simulated_dataset.csv')

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set the 'Date' column as the index
data.set_index('Date', inplace=True)

# Select the variables to include in the VAR model (excluding 'Win_Probability')
variables = ['Player_Ranking', 'Opponent_Ranking', 'Tournament_Ranking', 'Win_Probability']

# Calculate exponentially weighted moving averages of the selected variables
ewma_data = data[variables].ewm(span=3).mean()  # Adjust span as needed

# Fit the VAR model to the exponentially weighted moving averages
model = VAR(ewma_data)
var_result = model.fit()

# Forecast future values of the exponentially weighted moving averages using the VAR model
forecast_horizon = 1
forecast = var_result.forecast(ewma_data.values[-var_result.k_ar:], steps=forecast_horizon)

# Convert the forecasted values to a pandas DataFrame
forecast_df = pd.DataFrame(forecast, index=pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=forecast_horizon, freq='D'), columns=variables)

# Print the forecasted values
print("Forecasted Values:")
print(forecast_df)

# Plot the forecasted values of 'Win_Probability'
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Win_Probability'], label='Actual Win Probability')
plt.plot(forecast_df.index, forecast_df['Win_Probability'], linestyle='dashed', label='Forecasted Win Probability')
plt.title('VAR Forecast of Win Probability with Exponentially Weighted Moving Averages')
plt.xlabel('Date')
plt.ylabel('Win Probability')
plt.legend()
plt.show()
