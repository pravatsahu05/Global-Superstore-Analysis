import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def sales_forecasting(df):

    yearly_sales = df.groupby("Year")["Sales"].sum().reset_index()

    X = yearly_sales["Year"].values.reshape(-1,1)
    y = yearly_sales["Sales"]

    model = LinearRegression()
    model.fit(X,y)

    future_years = np.array([2025,2026,2027]).reshape(-1,1)

    predictions = model.predict(future_years)

    forecast_df = pd.DataFrame({
        "Year":[2025,2026,2027],
        "Predicted Sales":predictions
    })

    return forecast_df