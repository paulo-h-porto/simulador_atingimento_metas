import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --------- CONFIG GERAL ----------
st.set_page_config(page_title="Simulação de Metas 2025", layout="centered")

# --------- CSS CUSTOMIZADO ----------
st.markdown(
    """
    <style>
        /* Fundo da página */
        .stApp {
            background-color: #0a0a0a; /* fundo escuro elegante */
            color: #ffffff;
        }
        
        /* Header */
        .header {
            background-color: #103024;
            padding: 15px;
            border-radius: 12px; /* só header arredondado */
            text-align: center;
        }
        .header h1 {
            color: white;
            margin: 0;
        }

        /* Footer */
        .footer {
            background-color: #103024;
            padding: 10px;
            border-radius: 12px; /* só footer arredondado */
            text-align: center;
            margin-top: 40px;
            color: white;
            font-size: 0.9em;
        }

        /* Caixas internas (inputs, métricas, gráfico) */
        .block-container {
            border-radius: 0px !important; /* sem borda arredondada */
        }

        /* Caixa do metric */
        .stMetric {
            background-color: #e6ffe6;
            color: #000000;
            font-weight: bold;
            padding: 12px;
            border-radius: 0px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------- HEADER ----------
st.markdown('<div class="header"><h1>Simulação de Metas 2025</h1></div>', unsafe_allow_html=True)

# --------- INPUTS ----------
col1, col2, col3, col4 = st.columns(4)
with col1:
    meta = st.number_input("Meta:", value=100.0, step=0.1)
with col2:
    minimo = st.number_input("Patamar Mínimo:", value=70.0, step=0.1)
with col3:
    resultado = st.number_input("Resultado:", value=85.0, step=0.1)
with col4:
    sentido = st.selectbox("Sentido do Indicador:", ["Maior", "Menor"])

# --------- CÁLCULO ----------
if sentido == 'Maior':
    if resultado >= meta:
        atingimento = 100
    elif resultado <= minimo:
        atingimento = 0
    else:
        atingimento = ((resultado - minimo) / (meta - minimo)) * 100
else:
    if resultado <= meta:
        atingimento = 100
    elif resultado >= minimo:
        atingimento = 0
    else:
        atingimento = ((minimo - resultado) / (minimo - meta)) * 100

st.metric("Atingimento", f"{atingimento:.2f}%")

# --------- CURVA ----------
if sentido == 'Maior':
    x_curve = np.linspace(minimo, meta + (meta - minimo) * 0.5, 50)
    y_curve = np.interp(x_curve, [minimo, meta], [0, 100])
else:
    x_curve = np.linspace(meta - (minimo - meta) * 0.5, minimo, 50)
    y_curve = np.interp(x_curve, [meta, minimo], [100, 0])

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="Curva de Atingimento", line=dict(color="#103024")))
fig.add_trace(go.Scatter(x=[minimo], y=[0], mode='markers', name="Patamar Mínimo", marker=dict(color="red", size=10)))
fig.add_trace(go.Scatter(x=[meta], y=[100], mode='markers', name="Meta", marker=dict(color="green", size=10)))
fig.add_trace(go.Scatter(x=[resultado], y=[atingimento], mode='markers', name="Resultado", marker=dict(color="purple", size=10)))

fig.update_layout(
    xaxis_title="Valor do Indicador",
    yaxis_title="Atingimento (%)",
    yaxis=dict(range=[-5, 105]),
    plot_bgcolor="white"
)

st.subheader("Simulação de Atingimento de Meta")
st.plotly_chart(fig, use_container_width=True)

# --------- FOOTER ----------
st.markdown('<div class="footer">⚠️ Este painel é uma simulação e não substitui os resultados oficiais.</div>', unsafe_allow_html=True)
