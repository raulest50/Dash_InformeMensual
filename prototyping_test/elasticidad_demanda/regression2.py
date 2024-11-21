import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

def compute_elasticity_for_cities(data):
    # Create date column
    data['date'] = pd.to_datetime(data['anio'].astype(str) + '-' + data['mes'].astype(str) + '-01')

    # Filter data for date >= '2022-10-01'
    data_filtered = data[(data['date'] >= '2022-10-01') & (data['date'] <= '2024-08-01')]

    cities = data_filtered['ciudad'].unique()

    results = []

    for city in cities:
        city_data = data_filtered[data_filtered['ciudad'] == city]

        # Elasticity for 'corriente'
        if len(city_data) >= 2:
            X_corriente = np.log(city_data['precio_corriente'])
            y_corriente = np.log(city_data['vol_corriente'])
            if X_corriente.nunique() > 1:
                X_corriente_const = sm.add_constant(X_corriente)
                model_corriente = sm.OLS(y_corriente, X_corriente_const).fit()
                elasticity_corriente = model_corriente.params['precio_corriente']
                rsquared_corriente = model_corriente.rsquared  # Extract R-squared

                # Plot regression
                plt.figure()
                plt.scatter(X_corriente, y_corriente, label='Datos')
                plt.plot(X_corriente, model_corriente.predict(X_corriente_const), color='red', label='Ajuste')
                plt.title(f"Corriente - {city}")
                plt.xlabel('Log(Precio)')
                plt.ylabel('Log(Volumen)')
                plt.legend()
                plt.savefig(f'corriente_{city}.png')
                plt.close()
            else:
                elasticity_corriente = np.nan
                rsquared_corriente = np.nan
        else:
            elasticity_corriente = np.nan
            rsquared_corriente = np.nan

        # Elasticity for 'acpm'
        if len(city_data) >= 2:
            X_acpm = np.log(city_data['precio_acpm'])
            y_acpm = np.log(city_data['vol_acpm'])
            if X_acpm.nunique() > 1:
                X_acpm_const = sm.add_constant(X_acpm)
                model_acpm = sm.OLS(y_acpm, X_acpm_const).fit()
                elasticity_acpm = model_acpm.params['precio_acpm']
                rsquared_acpm = model_acpm.rsquared  # Extract R-squared

                # Plot regression
                plt.figure()
                plt.scatter(X_acpm, y_acpm, label='Datos')
                plt.plot(X_acpm, model_acpm.predict(X_acpm_const), color='red', label='Ajuste')
                plt.title(f"ACPM - {city}")
                plt.xlabel('Log(Precio)')
                plt.ylabel('Log(Volumen)')
                plt.legend()
                plt.savefig(f'acpm_{city}.png')
                plt.close()
            else:
                elasticity_acpm = np.nan
                rsquared_acpm = np.nan
        else:
            elasticity_acpm = np.nan
            rsquared_acpm = np.nan

        results.append({
            'ciudad': city,
            'elasticity_corriente': elasticity_corriente,
            'rsquared_corriente': rsquared_corriente,
            'elasticity_acpm': elasticity_acpm,
            'rsquared_acpm': rsquared_acpm
        })

    result_df = pd.DataFrame(results)
    return result_df

# Load the data
data = pd.read_csv("demanda_df.csv")

# Compute elasticity and get the result DataFrame
result_df = compute_elasticity_for_cities(data)

# Display the result
print(result_df)

# Save the result to CSV
result_df.to_csv("elasticities_till8.csv", index=False)
