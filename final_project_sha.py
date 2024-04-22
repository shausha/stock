# -*- coding: utf-8 -*-
"""final_project_sha.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_o41jPotZQ-73bV0BkBSxvCh-Cvm-ZaJ
"""

import pandas as pd
import missingno as msno

# Load the dataset
dataset = pd.read_csv('data.csv')

# Check for missing values
missing_values = dataset.isnull().sum()
print("Missing Values:\n", missing_values)

# Fill missing values with previous values
dataset.fillna(method='pad', inplace=True)

# Visualize missing values
msno.bar(dataset, figsize=(10, 5))

# Check missing values after filling
print("Missing Values After Filling:\n", dataset.isnull().sum())

import matplotlib.pyplot as plt
# Convert the 'Date' column to datetime format
dataset['Date'] = pd.to_datetime(dataset['Date'])

# Plot the closing price of the stock over time
plt.figure(figsize=(10, 5))
plt.plot(dataset['Date'], dataset['Close'], color='blue')
plt.title('Closing Price of Samsung Stock (2016-2021)')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.grid(True)
plt.show()

# Extract maximum and minimum closing prices along with dates
max_price = dataset.loc[dataset['Close'].idxmax()]
min_price = dataset.loc[dataset['Close'].idxmin()]

# Display random values of closing price along with dates
random_values = dataset.sample(n=5)
print("Random Values of Closing Price:")
print(random_values[['Date', 'Close']])

# Print maximum and minimum closing prices with dates
print("\nMaximum Closing Price:")
print(max_price[['Date', 'Close']])
print("\nMinimum Closing Price:")
print(min_price[['Date', 'Close']])

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Extract relevant features
X = dataset[['Open', 'Volume','High','Low']]  # Replace 'feature1', 'feature2', ... with your features
y = dataset['Close']  # Replace 'target' with your target variable

# Handle missing values
X.fillna(method='ffill', inplace=True)  # Forward fill missing values

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))

# Reshape the data for LSTM
time_steps = 100  # Adjust time steps as needed
X_reshaped = []
y_reshaped = []
for i in range(len(X_scaled) - time_steps):
    X_reshaped.append(X_scaled[i:i+time_steps])
    y_reshaped.append(y_scaled[i+time_steps])
X_reshaped, y_reshaped = np.array(X_reshaped), np.array(y_reshaped)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_reshaped, test_size=0.2, random_state=42)

from keras.models import Sequential
from keras.layers import LSTM, Dense
#Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(LSTM(units=50, return_sequences=True))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=64, validation_split=0.1)

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error,mean_absolute_percentage_error
import numpy as np

# Make predictions
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

# Inverse transform predictions
train_predictions_inv = scaler.inverse_transform(train_predictions.reshape(-1, 1))
y_train_inv = scaler.inverse_transform(y_train.reshape(-1, 1))
test_predictions_inv = scaler.inverse_transform(test_predictions.reshape(-1, 1))
y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))

y_range = np.max(y_train_inv) - np.min(y_train_inv)

# Calculate accuracy measures
#train
r2_score_train = r2_score(y_train_inv, train_predictions_inv)
rmse_score_train = np.sqrt(mean_squared_error(y_train_inv, train_predictions_inv))
normalized_rmse_train = rmse_score_train / y_range
mape_train = mean_absolute_percentage_error(y_train_inv, train_predictions_inv)

#test
r2_score_test = r2_score(y_test_inv, test_predictions_inv)
rmse_score_test = np.sqrt(mean_squared_error(y_test_inv, test_predictions_inv))
normalized_rmse_test = rmse_score_test / y_range
mape_test = mean_absolute_percentage_error(y_test_inv, test_predictions_inv)


# Print or visualize the accuracy measures
print("Training Set:")
print("R^2 Score:", r2_score_train)
print("Normalized RMSE:", normalized_rmse_train)
print("MAPE:", mape_train)

print("\nTesting Set:")
print("R^2 Score:", r2_score_test)
print("Normalized RMSE:", normalized_rmse_test)
print("MAPE:", mape_test)

from tabulate import tabulate

# Combine actual and predicted values into a list of tuples
data = [(actual[0], predicted[0]) for actual, predicted in zip(y_test_inv, test_predictions_inv)]

# Print as a table
print(tabulate(data, headers=['Actual', 'Predicted']))

import matplotlib.pyplot as plt

# Plot actual and predicted values
plt.figure(figsize=(10, 6))
plt.plot(y_test_inv, label='Actual')
plt.plot(test_predictions_inv, label='Predicted')
plt.xlabel('Sample Index')
plt.ylabel('Value')  # Corrected ylabel function
plt.title('Actual vs Predicted Values')
plt.legend()
plt.show()

import streamlit as st
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Streamlit app
st.title('Stock Price Prediction')

# Display metrics
st.write("MAPE:", mape_train)
st.write("Normalized RMSE:", normalized_rmse_train)
st.write("R^2 Score:", r2_score_train)

# Display actual vs predicted prices as a table
st.subheader('Actual vs Predicted Prices')
st.write(data)

pip install streamlit