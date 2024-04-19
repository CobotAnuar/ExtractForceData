import pandas as pd
import matplotlib.pyplot as plt
import re

def moving_average(data, window, fill_value=0):
  """
  Calculates the moving average of a pandas Series, replacing NaN with a specified value.

  Args:
    data: A pandas Series containing the data.
    window: The window size for the moving average.
    fill_value: The value to use for replacing NaN values (default: 0).

  Returns:
    A new pandas Series containing the moving average values with NaN replaced by the fill_value.
  """

  # Handle edge cases for window size exceeding data length
  if window > len(data):
    return data.rolling(window).mean()
  else:
    # Use shift to exclude the first (window-1) elements with NaN values
    return data.fillna(fill_value).rolling(window).mean().shift(window - 1)

def plot_data(dataframes):
  """
  Plots the data from a list of DataFrames.

  Args:
    dataframes: A list of DataFrames, where each DataFrame contains the data from a single test run.
  """
  for i, df in enumerate(dataframes):
    plt.figure(i+1)  # Create separate figure for each DataFrame
    plt.plot(df['timestamp'],df['ave_data'])  # Plot the 'data' column
    plt.title(f"Test Run {i+1}, [Kp, Ki, Kd]: [{df.attrs['Kp']}, {df.attrs['Ki']}, {df.attrs['Kd']}], Alpha:{df.attrs['alpha']}, Freq: {df.attrs['freq']:.3f}")
    #print(f"Test Run {i+1}, [Kp, Ki, Kd]: [{df['Kp']}, {df['Ki']}, {df['Kd']}], Alpha:{df['alpha']}")
    plt.xlabel("Timestamp (s)")
    plt.ylabel("Force")
    plt.grid(False)
    #plt.ylim(df['data'].min(), df['data'].max())
    plt.ylim(-35, -10)
  plt.show()

def parse_data(filename):
  """
  Parses data from a text file containing multiple test runs.

  Args:
    filename: The name of the file containing the data.

  Returns:
    A list of DataFrames, where each DataFrame contains the data from a single test run.
  """
  # Open the file and read its contents
  with open(filename, 'r') as f:
    data = f.read()
  # Split the data into separate test runs
  test_runs = data.split("--------\n")

  # Parse each test run into a DataFrame
  dataframes = []
  for run in test_runs:
    if run.strip():  # Skip empty runs
      lines = run.splitlines()
      data_lines = lines[:-8]  # Remove info lines at the bottom
      data_lines = [[i, float(s)] for i, s in enumerate(data_lines)]
      info_lines = lines[-7:]
      freq = float(info_lines[1].split('=')[-1].strip())
      alpha = float(info_lines[3].split('=')[-1].strip())
      Kp = float(info_lines[4].split('=')[-1].strip())
      Ki = float(info_lines[5].split('=')[-1].strip())
      Kd = float(info_lines[6].split('=')[-1].strip())
      df = pd.DataFrame(data_lines, columns=['index','data'])  # Set a generic column name
      df['timestamp'] = df['index']/freq
      window = freq
      df['ave_data'] = moving_average(df['data'], 3)
      df.attrs = {'Kp': Kp, 'Ki': Ki, 'Kd': Kd, 'alpha': alpha, 'freq': freq}
      print(df.attrs)
      dataframes.append(df)

  return dataframes


# Parse the data
dataframes = parse_data("Data\PIDSandingLog.txt")

# Print the dataframes
for i, df in enumerate(dataframes):
  print(f"Test Run {i+1}")
  print(df)
  print()

plot_data(dataframes)
