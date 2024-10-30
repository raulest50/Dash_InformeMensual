import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Read data from the Excel file
Elasticidad = pd.read_excel(
    "Elasticidad precio de la demanda.xlsx",
    sheet_name="Datos_R"
)

# View the DataFrame (optional)
print(Elasticidad.head())

# Subset the data (rows 32 to 56)
año_corrido = Elasticidad.iloc[31:56, :]  # Python is zero-indexed

# Log-transform the variables
año_corrido['log_volumen_corriente'] = np.log(año_corrido['volumen_corriente'])
año_corrido['log_precio_corriente'] = np.log(año_corrido['precio_corriente'])

# Prepare the data for the linear model
X = sm.add_constant(año_corrido['log_precio_corriente'])  # Adds a constant term to the predictor
y = año_corrido['log_volumen_corriente']

# Fit the linear model
modelo = sm.OLS(y, X).fit()

# Display the summary of the model
print(modelo.summary())

# Extract the coefficients
print("Coefficients:")
print(modelo.params)

# Create a scatter plot with a regression line
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x='log_precio_corriente',
    y='log_volumen_corriente',
    data=año_corrido,
    color='blue',
    label='Data Points'
)
sns.regplot(
    x='log_precio_corriente',
    y='log_volumen_corriente',
    data=año_corrido,
    scatter=False,
    color='red',
    label='Regression Line'
)
plt.xlabel('Log of Precio Corriente')
plt.ylabel('Log of Volumen Corriente')
plt.title('Linear Regression of Log-Transformed Variables')
plt.legend()
plt.show()

elasticidad_demanda = modelo.params['log_precio_corriente']
print(f"Elasticidad de la demanda: {elasticidad_demanda}")
