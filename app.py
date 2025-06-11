# import streamlit as st
# import matplotlib.pyplot as plt
# import pandas as pd

# # Charger les modules personnalisés
# from src.prediction import charger_donnees, entrainer_model, predire
# from src.simulateur_co2 import charger_et_calculer

# st.set_page_config(page_title="Dashboard Énergétique - VilleVerte", layout="wide")
# st.title("📊 Dashboard Énergétique - VilleVerte")

# # Sidebar : Sélection bâtiment
# st.sidebar.header("Paramètres")
# batiment_selectionne = st.sidebar.selectbox("Sélectionner un bâtiment", ["Mairie", "Ecole", "Gymnase"])
# nb_jours_prediction = st.sidebar.slider("Nombre de jours à prédire", 1, 7, 2)

# # Charger les données de consommation
# df_conso = charger_et_calculer("data/Consommation_simule_VilleVerte_ademe.csv")

# # Filtrer par bâtiment
# df_batiment = df_conso[df_conso["batiment"] == batiment_selectionne]

# # Afficher la consommation récente
# st.subheader(f"📈 Consommation électrique - {batiment_selectionne}")
# st.line_chart(df_batiment.set_index('datetime')['consommation_kwh'])

# # Afficher l'empreinte carbone
# st.subheader(f"🌍 Émissions de CO₂ - {batiment_selectionne}")
# st.line_chart(df_batiment.set_index('datetime')['emission_co2_kg'])

# # Prédiction énergétique
# st.subheader(f"🔮 Prédiction de consommation - {batiment_selectionne}")

# # Charger les données pour Prophet
# df_prophet = charger_donnees("data/Consommation_simul_e_VilleVerte.csv", batiment_selectionne)
# model = entrainer_model(df_prophet)
# forecast = predire(model, periods=nb_jours_prediction*24)

# fig = model.plot_components(forecast)
# st.pyplot(fig)

# # Comparaison avant/après simulation
# st.sidebar.subheader("Simulation Scénario")
# reduction_pourcentage = st.sidebar.slider("Réduction de consommation (%)", 0, 100, 0)

# if reduction_pourcentage > 0:
#     df_batiment['conso_apres'] = df_batiment['consommation_kwh'] * (1 - reduction_pourcentage / 100)
#     df_batiment['emission_apres'] = df_batiment['conso_apres'] * df_batiment['taux_co2_g_kwh'] / 1000

#     gain_carbone = df_batiment['emission_co2_kg'].sum() - df_batiment['emission_apres'].sum()
#     st.success(f"✅ Gain estimé : {gain_carbone:.2f} kg CO₂ économisés sur la période.")

#     fig, ax = plt.subplots()
#     df_batiment.set_index('datetime')[['consommation_kwh', 'conso_apres']].plot(ax=ax)
#     st.pyplot(fig)

# # Export CSV
# if st.sidebar.button("Exporter en CSV"):
#     df_batiment.to_csv(f"export_{batiment_selectionne}.csv", index=False)
#     st.success("Fichier exporté.")

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from src.prediction import charger_donnees, entrainer_model, predire
from src.simulateur_co2 import charger_et_calculer

st.set_page_config(page_title="Dashboard Énergétique - VilleVerte", layout="wide")
st.title(" Dashboard Énergétique - VilleVerte")

st.sidebar.header("Paramètres")
batiment_selectionne = st.sidebar.selectbox("Sélectionner un bâtiment", ["Mairie", "Ecole", "Gymnase"])
nb_jours_prediction = st.sidebar.slider("Nombre de jours à prédire", 1, 7, 2)

df_conso = charger_et_calculer("data/Consommation_simule_VilleVerte_ademe.csv")
df_batiment = df_conso[df_conso["batiment"] == batiment_selectionne]

st.subheader(f" Consommation électrique & {batiment_selectionne}")
st.line_chart(df_batiment.set_index('datetime')['consommation_kwh'])

st.subheader(f" Émissions de CO₂ - {batiment_selectionne}")
st.line_chart(df_batiment.set_index('datetime')['emission_co2_kg'])

st.subheader(f" Prédiction de consommation - {batiment_selectionne}")
df_arima = charger_donnees("data/Consommation_simule_VilleVerte_ademe.csv", batiment_selectionne)
model = entrainer_model(df_arima)
forecast = predire(model, periods=nb_jours_prediction * 24)

forecast_index = pd.date_range(start=df_arima.index[-1] + pd.Timedelta(hours=1), periods=nb_jours_prediction * 24, freq='H')
forecast_df = pd.DataFrame({'forecast': forecast}, index=forecast_index)
st.line_chart(forecast_df)

st.sidebar.subheader("Simulation Scénario")
reduction_pourcentage = st.sidebar.slider("Réduction de consommation (%)", 0, 100, 0)

if reduction_pourcentage > 0:
    df_batiment['conso_apres'] = df_batiment['consommation_kwh'] * (1 - reduction_pourcentage / 100)
    df_batiment['emission_apres'] = df_batiment['conso_apres'] * df_batiment['taux_co2_g_kwh'] / 1000

    gain_carbone = df_batiment['emission_co2_kg'].sum() - df_batiment['emission_apres'].sum()
    st.success(f"✅ Gain estimé : {gain_carbone:.2f} kg CO₂ économisés sur la période.")

    fig, ax = plt.subplots()
    df_batiment.set_index('datetime')[['consommation_kwh', 'conso_apres']].plot(ax=ax)
    st.pyplot(fig)

if st.sidebar.button("Exporter en CSV"):
    df_batiment.to_csv(f"export_{batiment_selectionne}.csv", index=False)
    st.success("Fichier exporté.")
