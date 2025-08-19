# import streamlit as st
# import plotly.graph_objects as go
# import numpy as np

# # --------- CONFIG GERAL ----------
# st.set_page_config(
#     page_title="Simulação de Metas 2025",
#     page_icon="📊",
#     layout="centered",
#     initial_sidebar_state="collapsed",
# )

# # --------- CSS CUSTOMIZADO ----------
# st.markdown(
#     """
#     <style>
#         .stApp { background-color: #0a0a0a; color: #ffffff; }
#         .header { margin: 0px 0px 20px; background-color: #103024; padding: 15px; border-radius: 12px; text-align: center; }
#         .header h1 { color: white; margin: 0; }
#         .footer { background-color: #103024; padding: 10px; border-radius: 12px; text-align: center; margin-top: 40px; color: white; font-size: 0.9em; }
#         .block-container { border-radius: 0px !important; }
#         .stMetric { margin: 15px 0px; border-radius: 12px; background-color: #103024; color: #103024; font-weight: bold; padding: 12px; border-radius: 0px !important; }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # --------- HEADER ----------
# st.markdown('<div class="header"><h1>Simulação de Metas 2025</h1></div>', unsafe_allow_html=True)

# # --------- INPUTS ----------
# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     meta = st.number_input("Meta:", value=100.0, step=1.0)
# with col2:
#     realizado = st.number_input("Realizado:", value=80.0, step=1.0)
# with col3:
#     minimo = st.number_input("Patamar Mínimo:", value=45.0, step=1.0)
# with col4:
#     sentido = st.selectbox("Sentido do Indicador:", ["Maior", "Menor"])

# # --------- CÁLCULO DE RESULTADO ----------
# if realizado == meta:
#     resultado = 100
# elif sentido == "Maior":
#     resultado = realizado / meta * 100
# else: resultado = (((meta - realizado) / meta) + 1) * 100

# st.metric("Resultado", f"{resultado:.2f}%")
# # --------- CÁLCULO DE ATINGIMENTO CORRIGIDO ----------
# y_minimo = 45  # Patamar mínimo sempre = 45%
# y_meta = 100   # Meta = 100%

# # if 
# # sentido == "Maior":  # melhor para cima
#     # m = (y_meta - y_minimo) / (meta - minimo)

# if resultado < minimo:
#     atingimento = 0
# else:
#     m = (y_meta - y_minimo) / (y_meta - minimo)
#     b = y_minimo - m * minimo
#     atingimento = b + m * resultado
    
# # else:  # melhor para baixo
# #     # Inverter a reta: quanto menor o realizado, maior o atingimento
# #     m = (y_minimo - y_meta) / (minimo - meta)  # inclinação negativa
# #     b = y_meta - m * meta
# #     if realizado > minimo:
# #         atingimento = 0
# #     else:
# #         atingimento = b + m * realizado

# atingimento = max(0, min(atingimento, 120))  # limitar entre 0 e 120
# st.metric("Atingimento", f"{atingimento:.2f}%")

# # --------- CURVA CORRIGIDA PARA PLOT ---------
# # if sentido == "Maior":

# x_curve = np.linspace(minimo, meta, 50)
# y_curve = y_minimo + (y_meta - y_minimo) * (x_curve - minimo) / (meta - minimo)

# # else:  # Menor
# #     x_curve = np.linspace(meta, minimo, 50)  # inverte o eixo X
# #     y_curve = y_meta + (y_minimo - y_meta) * (x_curve - meta) / (minimo - meta)
    
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="Curva de Atingimento", line=dict(color="#103024")))
# fig.add_trace(go.Scatter(x=[minimo], y=[y_minimo], mode='markers', name="Patamar Mínimo", marker=dict(color="red", size=10)))
# fig.add_trace(go.Scatter(x=[meta], y=[100], mode='markers', name="Meta", marker=dict(color="green", size=10)))
# fig.add_trace(go.Scatter(x=[resultado], y=[atingimento], mode='markers', name="Resultado", marker=dict(color="purple", size=10)))

# # Ajuste dos limites do eixo X
# x_min = min(meta, minimo) - 5
# x_max = max(meta, minimo) + 5


# fig.update_layout(
    
#     # xaxis_title="Valor do Indicador",
#     xaxis_title="Resultado (%)",
#     yaxis_title="Atingimento (%)",
#     xaxis=dict(range=[0, 140], showgrid=False),
#     yaxis=dict(range=[0, 140], showgrid=False),
#     plot_bgcolor="white"
# )

# st.subheader("Simulação de Atingimento de Meta")
# st.plotly_chart(fig, use_container_width=True)


import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --------- CONFIG GERAL ----------
st.set_page_config(
    page_title="Simulação de Metas 2025",
    page_icon="📊",
    layout="wide",
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
        .controls-container { background-color: #1a1a1a; padding: 20px; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True
)

# --------- HEADER ----------
st.markdown('<div class="header"><h1>Simulação de Metas 2025</h1></div>', unsafe_allow_html=True)

# --------- LAYOUT PRINCIPAL ----------
col_controls, col_chart = st.columns([1, 3])  # 1:3 ratio

# --------- CONTROLES NA COLUNA DA ESQUERDA ----------
with col_controls:
    st.markdown('<div class="controls-container">', unsafe_allow_html=True)
    
    st.subheader("Parâmetros")
    sentido = st.selectbox("Sentido do Indicador:", ["Maior", "Menor"])
    minimo = st.number_input("Patamar Mínimo:", value=45.0, step=1.0)
    meta = st.number_input("Meta:", value=100.0, step=1.0)
    realizado = st.number_input("Realizado:", value=80.0, step=1.0)
    
    # --------- CÁLCULO DE RESULTADO ----------
    if realizado == meta:
        resultado = 100
    elif sentido == "Maior":
        resultado = realizado / meta * 100
    else: 
        resultado = (((meta - realizado) / meta) + 1) * 100

    st.metric("Resultado", f"{resultado:.2f}%")
    
    # --------- CÁLCULO DE ATINGIMENTO CORRIGIDO ----------
    y_minimo = 45  # Patamar mínimo sempre = 45%
    y_meta = 100   # Meta = 100%

    if resultado < minimo:
        atingimento = 0
    else:
        m = (y_meta - y_minimo) / (y_meta - minimo)
        b = y_minimo - m * minimo
        atingimento = b + m * resultado
        
    atingimento = max(0, min(atingimento, 120))  # limitar entre 0 e 120
    st.metric("Atingimento", f"{atingimento:.2f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --------- GRÁFICO NA COLUNA DA DIREITA ----------
with col_chart:
    # --------- CURVA CORRIGIDA PARA PLOT ---------
    x_curve = np.linspace(minimo, meta, 50)
    y_curve = y_minimo + (y_meta - y_minimo) * (x_curve - minimo) / (meta - minimo)
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="Curva de Atingimento", line=dict(color="#103024")))
    fig.add_trace(go.Scatter(x=[minimo], y=[y_minimo], mode='markers', name="Patamar Mínimo", marker=dict(color="red", size=10)))
    fig.add_trace(go.Scatter(x=[meta], y=[100], mode='markers', name="Meta", marker=dict(color="green", size=10)))
    fig.add_trace(go.Scatter(x=[resultado], y=[atingimento], mode='markers', name="Resultado", marker=dict(color="purple", size=10)))

    fig.update_layout(
        xaxis_title="Resultado (%)",
        yaxis_title="Atingimento (%)",
        xaxis=dict(range=[0, 140], showgrid=False),
        yaxis=dict(range=[0, 140], showgrid=False),
        plot_bgcolor="white",
        height=500  # Ajuste a altura para melhor visualização
    )

    st.subheader("Simulação de Atingimento de Meta")
    st.plotly_chart(fig, use_container_width=True)

# --------- FOOTER ----------
st.markdown('<div class="footer">⚠️ Este painel é uma simulação e não substitui os resultados oficiais.</div>', unsafe_allow_html=True)
