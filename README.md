# Time Series Analysis Dashboard

A **Time Series Analysis Dashboard** built using Python and Dash, designed for interactive data visualization, model fitting, and forecasting. This project leverages powerful forecasting models from **Nixtla's `statsforecast` package** and integrates them into a user-friendly, web-based application.

https://github.com/user-attachments/assets/93eb6dde-f55f-4d6b-b5db-2e4f761afd76

## Features

### Data Upload and Management

- **Upload CSV files**: Allows users to upload time series data directly into the app.
- **Data clearing**: Remove previously uploaded data to reset the dashboard.

### Interactive Graphs and Visualizations

- **Training, Testing, and Forecast Visualization**: Split your data into training and testing sets and visualize the results along with the forecast.
- **Dynamic Forecast Display**: Choose from multiple models (e.g., AutoARIMA, HoltWinters) to display forecasted values.
- **Adjustable Slider**: Set the split point for training and testing datasets dynamically using a slider.

### Model Fitting and Forecasting

- **Built-in Forecasting Models**:
  - AutoARIMA
  - HoltWinters
  - SeasonalNaive
  - HistoricAverage
- **Parameter Tuning**: Modify hyperparameters like `freq` and `season_length` directly in the app.
- **Real-time Loading Animation**: Provides visual feedback while forecasts are being calculated.

## Technologies Used

- **Dash**: Framework for building interactive web applications in Python.
- **Plotly**: Library for creating interactive plots.
- **Pandas**: Data manipulation and analysis.
- **Nixtla's `statsforecast`**: State-of-the-art time series forecasting package.
- **Dash Bootstrap Components**: For responsive and aesthetic UI components.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TimeSeries-Analysis.git
   cd TimeSeries-Analysis
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app
   ```bash
   python app.py
   ```
4. Open the app in your browser at `http://127.0.0.1:8050/`

## Usage

1. **Upload your time series data** via the **Upload Modal**.
2. **Adjust the training and testing split** using the **slider**.
3. **Select a forecasting model** from the dropdown and fine-tune parameters if needed.
4. **View forecasts** alongside training and testing data in the interactive graph.

## Data Format

The uploaded data should have the following structure:

| **unique_id** | **ds**           | **y**  |
| ------------- | ---------------- | ------ |
| A             | 2019-09-01 12:00 | 123.45 |

- **`unique_id`**: Identifier for the time series (e.g., product ID or location).
- **`ds`**: Date column in `YYYY-MM-DD HH:MM:SS` format for hourly data or `YYYY-MM-DD` for daily.
- **`y`**: Observed values for the time series.

## Known Issues

- Data format mismatches (e.g., `ds` column format) may cause errors.
- Ensure hyperparameters match the dataset characteristics.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
