import streamlit as st
import scipy.stats
import pandas as pd
import time

# 🧭 Estado entre ejecuciones: para contar experimentos y guardar resultados
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

# ✨ Título de la app
st.header('Lanzar una moneda')

# 🎚️ Slider y botón de ejecución
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

# 📈 Crear gráfico inicial
chart = st.line_chart([0.5])

# 🔍 Función que simula el experimento y actualiza la media en cada intento
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

# 🚀 Ejecución del experimento
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    # Guardar resultados en el historial
    resultado = pd.DataFrame(
        [[st.session_state['experiment_no'], number_of_trials, mean]],
        columns=['no', 'iteraciones', 'media']
    )

    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], resultado],
        ignore_index=True
    )

# 📜 Mostrar tabla de resultados anteriores
st.write(st.session_state['df_experiment_results'])