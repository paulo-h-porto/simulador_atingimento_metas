import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --------- CONFIG GERAL ----------
st.set_page_config(
    page_title="Simulação de Metas 2025",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --------- CSS CUSTOMIZADO ----------
st.markdown(
    """
    <style>
        .stApp { background-color: #0a0a0a; color: #ffffff; }
        .header { margin: 0px 0px 20px; background-color: #103024; padding: 15px; border-radius: 12px; text-align: center; }
        .header h1 { color: white; margin: 0; }
        .footer { background-color: #103024; padding: 10px; border-radius: 12px; text-align: center; margin-top: 40px; color: white; font-size: 0.9em; }
        .block-container { border-radius: 0px !important; }
        .stMetric { margin: 15px 0px; border-radius: 12px; background-color: #103024; color: #103024; font-weight: bold; padding: 12px; border-radius: 0px !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# --------- HEADER ----------
st.markdown('<div class="header"><h1>Simulação de Metas 2025</h1></div>', unsafe_allow_html=True)

# --------- INPUTS ----------
col1, col2, col3, col4 = st.columns(4)
with col1:
    meta = st.number_input("Meta:", value=100.0, step=1.0)
with col2:
    realizado = st.number_input("Realizado:", value=80.0, step=1.0)
with col3:
    minimo = st.number_input("Patamar Mínimo:", value=45.0, step=1.0)
with col4:
    sentido = st.selectbox("Sentido do Indicador:", ["Maior", "Menor"])

# --------- CÁLCULO DE RESULTADO ----------
if sentido == "Maior":
    resultado = realizado / meta
else:  # Menor
    resultado = ((meta - realizado) / meta) + 1

# --------- CÁLCULO DE ATINGIMENTO ----------
if sentido == "Maior":
    m = (1 - 0) / (meta - minimo)  # inclinação da reta
    b = 0 - m * minimo             # intercepto
    atingimento_calc = b + m * realizado
else:  # Menor
    m = (0 - 1) / (meta - minimo)
    b = 1 - m * minimo
    atingimento_calc = b + m * realizado

atingimento = atingimento_calc * 100
atingimento = max(0, min(atingimento, 120))  # limitar entre 0 e 120

st.metric("Atingimento", f"{atingimento:.2f}%")

# --------- CURVA ----------
if sentido == 'Maior':
    x_curve = np.linspace(minimo, meta + (meta - minimo) * 0.5, 50)
    y_curve = np.interp(x_curve, [minimo, meta], [45, 100])
else:
    x_curve = np.linspace(meta - (minimo - meta) * 0.5, minimo, 50)
    y_curve = np.interp(x_curve, [meta, minimo], [100, 45])

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="Curva de Atingimento", line=dict(color="#103024")))
fig.add_trace(go.Scatter(x=[minimo], y=[0], mode='markers', name="Patamar Mínimo", marker=dict(color="red", size=10)))
fig.add_trace(go.Scatter(x=[meta], y=[100], mode='markers', name="Meta", marker=dict(color="green", size=10)))
fig.add_trace(go.Scatter(x=[realizado], y=[atingimento], mode='markers', name="Resultado", marker=dict(color="purple", size=10)))

# --------- LAYOUT DO GRÁFICO ----------
y_max = max(120, atingimento + 10)
y_min = max(0, minimo - 10)
fig.update_layout(
    xaxis_title="Valor do Indicador",
    yaxis_title="Atingimento (%)",
    yaxis=dict(range=[y_min, y_max], showgrid=False),
    xaxis=dict(showgrid=False),
    plot_bgcolor="white"
)

st.subheader("Simulação de Atingimento de Meta")
st.plotly_chart(fig, use_container_width=True)

# --------- FOOTER ----------
st.markdown('<div class="footer">⚠️ Este painel é uma simulação e não substitui os resultados oficiais.</div>', unsafe_allow_html=True)
