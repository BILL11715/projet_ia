# from fbprophet import Prophet
# import pandas as pd

# def charger_donnees(path, batiment):
#     df = pd.read_csv(path)
#     df['ds'] = pd.to_datetime(df['datetime'])
#     df['y'] = df['consommation_kwh']
#     df = df[df['batiment'] == batiment]
#     return df[['ds', 'y']]

# def entrainer_model(df):
#     model = Prophet(
#         yearly_seasonality=False,
#         weekly_seasonality=True,
#         daily_seasonality=True
#     )
#     model.add_country_holidays(country_name='FR')
#     model.fit(df)
#     return model

# def predire(model, periods=48):  # 2 jours x 24h
#     future = model.make_future_dataframe(periods=periods, freq='H')
#     forecast = model.predict(future)
#     return forecast
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def charger_donnees(path, batiment):
    df = pd.read_csv(path, parse_dates=["Datetime"])
    df = df[df["Batiment"] == batiment]
    df.index = pd.to_datetime(df["Datetime"])
    return df

def entrainer_model(df):
    model = ARIMA(df["Consommation (kWh)"], order=(1, 1, 1))
    model_fit = model.fit()
    return model_fit

def predire(model, periods=48):
    forecast = model.forecast(steps=periods)
    return forecast
