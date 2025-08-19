import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Simulação de Metas 2025",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Styles (simple CSS) ----------
st.markdown(
    """
    <style>
    .main { background: #ffffff; }
    .stMetric { background: #ddffe3; padding: 8px 12px; border-radius: 12px; }
    .card { background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); padding: 16px; margin-top: 10px; }
    .header { background: #103024; color: white; padding: 16px; border-radius: 12px; text-align: center; font-weight: 700; font-size: 22px; }
    .footer { background: #ddffe3; color: #2b2d2c; padding: 12px; text-align: center; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="header">Simulação de Metas 2025</div>', unsafe_allow_html=True)

# ---------- Inputs ----------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cols = st.columns([1,1,1,1.2])

    with cols[0]:
        meta = st.number_input("Meta:", value=100.0, step=0.1, format="%.2f")
    with cols[1]:
        minimo = st.number_input("Patamar Mínimo:", value=70.0, step=0.1, format="%.2f")
    with cols[2]:
        resultado = st.number_input("Resultado:", value=85.0, step=0.1, format="%.2f")
    with cols[3]:
        sentido = st.selectbox(
            "Sentido do Indicador:",
            ["Maior", "Menor"],
            index=0,
            help="Maior: quanto maior melhor. Menor: quanto menor melhor.",
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Calculation ----------
def calcular_atingimento(meta, minimo, resultado, sentido):
    # Proteções contra valores inválidos
    if meta is None or minimo is None or resultado is None:
        return 0.0
    if meta == minimo:
        return 100.0 if resultado >= meta and sentido == "Maior" else (100.0 if resultado <= meta and sentido == "Menor" else 0.0)

    if sentido == "Maior":
        if resultado >= meta:
            return 100.0
        elif resultado <= minimo:
            return 0.0
        else:
            return ((resultado - minimo) / (meta - minimo)) * 100.0
    else:  # Menor
        if resultado <= meta:
            return 100.0
        elif resultado >= minimo:
            return 0.0
        else:
            return ((minimo - resultado) / (minimo - meta)) * 100.0

atingimento = float(calcular_atingimento(meta, minimo, resultado, sentido))

# ---------- Metric ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.metric("Atingimento", f"{atingimento:.2f}%")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Curve & Chart ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
if sentido == "Maior":
    x_curve = np.linspace(minimo, meta + (meta - minimo) * 0.5, 50)
    y_curve = np.interp(x_curve, [minimo, meta], [0, 100])
    # Extend flat at 100% after meta
    x_curve = np.concatenate([x_curve, [meta + (meta - minimo) * 0.5]])
    y_curve = np.concatenate([y_curve, [100]])
else:
    x_curve = np.linspace(meta - (minimo - meta) * 0.5, minimo, 50)
    y_curve = np.interp(x_curve, [meta, minimo], [100, 0])
    # Extend flat at 100% before meta
    x_curve = np.concatenate([[meta - (minimo - meta) * 0.5], x_curve])
    y_curve = np.concatenate([[100], y_curve])

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_curve, y=y_curve, mode="lines",
    name="Curva de Atingimento",
    line=dict(color="#103024", width=2),
))
fig.add_trace(go.Scatter(
    x=[minimo], y=[0], mode="markers",
    name="Patamar Mínimo",
    marker=dict(color="#c50000", size=12),
))
fig.add_trace(go.Scatter(
    x=[meta], y=[100], mode="markers",
    name="Meta",
    marker=dict(color="#00c853", size=12),
))
fig.add_trace(go.Scatter(
    x=[resultado], y=[atingimento], mode="markers",
    name="Resultado",
    marker=dict(color="purple", size=14, line=dict(width=2, color="black")),
))

fig.update_layout(
    title="Simulação de Atingimento de Meta",
    title_font=dict(size=20, color="#103024"),
    xaxis_title="Valor do Indicador",
    yaxis_title="Atingimento (%)",
    font=dict(color="#2b2d2c"),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    hovermode="x unified",
    margin=dict(l=40, r=40, t=40, b=40),
    legend=dict(bordercolor="#ddd", borderwidth=1, bgcolor="white"),
)
fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", range=[-5, 105])

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Help text ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(
    """
    **Como interpretar:**
    - **Meta (verde)** → Valor desejado (100% de atingimento)  
    - **Patamar mínimo (vermelho)** → Valor mínimo aceitável (0% de atingimento)  
    - **Resultado (roxo)** → Valor atual do indicador  
    - **Linha verde-escura** → Relação entre valores e percentual de atingimento  

    _Observação: este simulador segue a mesma lógica aplicada no painel oficial de metas._
    """.strip()
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Este painel é uma simulação e não substitui os resultados oficiais.</div>', unsafe_allow_html=True)