# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# Function to compute elasticity and plot for a given product
def compute_elasticity(data, selected_city, product_name, volume_col, price_col):
    # Filter data for the selected city
    city_data = data[data['ciudad'] == selected_city.upper()]

    # Ensure there is data available for the selected city
    if city_data.empty:
        print(f"No data available for the selected city: {selected_city}")
        return None

    # Filter data for non-missing values
    product_data = city_data[[volume_col, price_col]].dropna()
    product_data = product_data[(product_data[volume_col] > 0) & (product_data[price_col] > 0)]

    # Check if there are enough data points
    if len(product_data) < 2:
        print(f"Not enough data points for {product_name} in {selected_city}")
        return None

    # Compute logarithms
    product_data['log_volume'] = np.log(product_data[volume_col])
    product_data['log_price'] = np.log(product_data[price_col])

    # Perform linear regression
    X = sm.add_constant(product_data['log_price'])  # Adds a constant term to the predictor
    y = product_data['log_volume']
    model = sm.OLS(y, X).fit()
    elasticity = model.params['log_price']

    # Print the summary of the model
    print(f"\nAnalyzing '{product_name}' product in {selected_city}:\n")
    print(model.summary())

    # Interpret the elasticity
    elasticity_value = elasticity
    print("\n===========================================")
    print(f"Elasticity of demand for {product_name} in {selected_city}:")
    print(f"Elasticity (coefficient of log_price): {elasticity_value:.4f}")
    if abs(elasticity_value) > 1:
        interpretation = "The demand is elastic (very sensitive to price changes)."
    elif abs(elasticity_value) < 1:
        interpretation = "The demand is inelastic (not very sensitive to price changes)."
    else:
        interpretation = "The demand has unitary elasticity."
    print(f"Interpretation: {interpretation}")
    print("===========================================")

    # Plot the data with regression line
    plt.figure()
    sns.regplot(x='log_price', y='log_volume', data=product_data, ci=None,
                line_kws={'color': 'red'})
    plt.title(f"Log-Log Plot of Volume vs Price for {product_name} in {selected_city}")
    plt.xlabel("Log(Price)")
    plt.ylabel("Log(Volume)")
    plt.show()

    return {'model': model, 'elasticity': elasticity_value}


data = pd.read_csv("demanda_df.csv")

data = data.sort_values(by=['ciudad', 'anio', 'mes'])
data.to_csv("sorted_merged.csv", index=False)


available_cities = data['ciudad'].unique()
print("\nAvailable cities:")
print(available_cities)

# Set the selected city directly
selected_city = 'NACIONAL'

# Compute elasticity for 'CORRIENTE'
corriente_results = compute_elasticity(
    data,
    selected_city=selected_city,
    product_name="CORRIENTE",
    volume_col="vol_corriente",
    price_col="precio_corriente"
)

# Compute elasticity for 'ACPM'
acpm_results = compute_elasticity(
    data,
    selected_city=selected_city,
    product_name="ACPM",
    volume_col="vol_acpm",
    price_col="precio_acpm"
)