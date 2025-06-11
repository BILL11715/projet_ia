# import pandas as pd

# def calculer_emission(row):
#     return row['consommation_kwh'] * row['taux_co2_g_kwh'] / 1000

# def charger_et_calculer(path, taux_co2_par_defaut=450):
#     df = pd.read_csv(path)
#     df.columns = ['datetime', 'batiment', 'consommation_kwh', 'taux_co2_g_kwh', 'emission_co2_kg']

#     # Si le taux n'est pas présent, on applique une valeur par défaut
#     if df['taux_co2_g_kwh'].isna().all():
#         df['taux_co2_g_kwh'] = taux_co2_par_defaut

#     df['datetime'] = pd.to_datetime(df['datetime'])
#     df['emission_co2_kg'] = df.apply(calculer_emission, axis=1)
#     return df
import pandas as pd

def calculer_emission(row):
    return row['consommation_kwh'] * row['taux_co2_g_kwh'] / 1000

def charger_et_calculer(path, taux_co2_par_defaut=450):
    df = pd.read_csv(path)

    # Adapter dynamiquement les noms de colonnes
    if len(df.columns) == 4:
        df.columns = ['Datetime', 'Batiment', 'Consommation (kWh)', 'Emission CO2 (kg)']
    elif len(df.columns) == 5:
        df.columns = ['datetime', 'batiment', 'consommation_kwh', 'taux_co2_g_kwh', 'emission_co2_kg']

    if df['taux_co2_g_kwh'].isna().all():
        df['taux_co2_g_kwh'] = taux_co2_par_defaut

    df['datetime'] = pd.to_datetime(df['datetime'])
    df['emission_co2_kg'] = df.apply(calculer_emission, axis=1)
    return df
