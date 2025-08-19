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
# --------- CURVA E PONTOS COM VISUAL DO GRÁFICO ----------
fig = go.Figure()

# Curva de atingimento
if sentido == 'Maior':
    x_curve = np.linspace(minimo, meta + (meta - minimo) * 0.5, 50)
    y_curve = np.interp(x_curve, [minimo, meta], [minimo, 100])
else:
    x_curve = np.linspace(meta - (minimo - meta) * 0.5, minimo, 50)
    y_curve = np.interp(x_curve, [meta, minimo], [100, minimo])

fig.add_trace(go.Scatter(
    x=x_curve,
    y=y_curve,
    mode='lines',
    name="Reta do Atingimento",
    line=dict(color="#1f774e", width=3)
))

# Pontos: Patamar Mínimo, Meta e Realizado
fig.add_trace(go.Scatter(
    x=[minimo], y=[minimo if sentido=="Maior" else 100],
    mode='markers+text',
    name="Patamar Mínimo",
    marker=dict(color="red", size=12),
    text=[f"{int(minimo)}%"], textposition="top center"
))
fig.add_trace(go.Scatter(
    x=[meta], y=[100],
    mode='markers+text',
    name="Meta",
    marker=dict(color="green", size=12),
    text=["100%"], textposition="top center"
))
fig.add_trace(go.Scatter(
    x=[realizado], y=[atingimento],
    mode='markers+text',
    name="Realizado",
    marker=dict(color="blue", size=12),
    text=[f"{atingimento:.0f}%"], textposition="top center"
))

# Layout
fig.update_layout(
    title="Reta do Atingimento",
    xaxis_title="Resultado",
    yaxis_title="Atingimento",
    xaxis=dict(tickformat=".0%", range=[0, 1.2*meta/100]),
    yaxis=dict(tickformat=".0%", range=[0, 120]),
    plot_bgcolor="white",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


# --------- FOOTER ----------
st.markdown('<div class="footer">⚠️ Este painel é uma simulação e não substitui os resultados oficiais.</div>', unsafe_allow_html=True)
