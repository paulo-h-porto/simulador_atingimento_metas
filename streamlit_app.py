
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
        # .stApp { 
        #     background-color: #0a0a0a; 
        #     color: #ffffff; }
        .header { 
            margin: 0px 0px 20px; 
            # background-color: #103024; 
            background-color: #1b4c22;
            padding: 15px; 
            border-radius: 12px; 
            text-align: center; }
        .header h1 { 
            color: white; 
            margin: 0; }
        .footer { 
            background-color: #103024; 
            padding: 10px; 
            border-radius: 12px; 
            text-align: center; 
            margin-top: 40px; 
            color: white; 
            font-size: 0.9em; }
        .block-container { 
            border-radius: 0px !important; }
        .controls-container { 
            background-color: #1a1a1a; 
            padding: 10px; 
            border-radius: 12px; }
        .section-title { 
            text-align: center; 
            margin-bottom: 20px; 
            background-color: #d7e1de;
            border-radius: 12px; 
            color: #2b2d2c; }
        .metric-resultado {
            background-color: #d7e1de !important;
            color: white !important;
            padding: 5px;
            border-radius: 10px;
            # border-left: 5px solid #d7e1de;
            # margin: 15px 0px; 
            }
        .metric-label-resultado {
            font-size: 0.9em;
            text-align: center; 
            # font-weight: bold;
            color: #2b2d2c; }
        .metric-value-resultado {
            font-size: 1.2em;
            text-align: center; 
            font-weight: bold;
            color: #2b2d2c; }
        .metric-atingimento {
            background-color: #2d5016 !important;
            color: white !important;
            padding: 10px;
            border-radius: 10px;
            border-left: 5px solid #169a00;
            margin: 10px 0px; }
        .metric-label-atingimento {
            font-size: 1.1em;
            text-align: center; 
            font-weight: bold;
            color: white; }
        .metric-value-atingimento {
            font-size: 1.8em;
            text-align: center; 
            font-weight: bold;
            color: white; }
        .params-container {
            background-color: #2a2a2a;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px; }
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
    
    # Subtítulo centralizado para Parâmetros
    st.markdown('<div class="section-title"><h3>Parâmetros</h3></div>', unsafe_allow_html=True)
    
    # Container para os parâmetros
    sentido = st.selectbox("Sentido do Indicador:", ["Maior", "Menor"])
    minimo = st.number_input("Patamar Mínimo:", value=45.0, step=1.0)
    meta = st.number_input("Meta:", value=100.0, step=1.0)
    realizado = st.number_input("Realizado:", value=80.0, step=1.0)
    # st.markdown('</div>', unsafe_allow_html=True)
    
    # --------- CÁLCULO DE RESULTADO ----------
    if realizado == meta:
        resultado = 100
    elif sentido == "Maior":
        resultado = realizado / meta * 100
    else: 
        resultado = (((meta - realizado) / meta) + 1) * 100

    
    # --------- CÁLCULO DE ATINGIMENTO CORRIGIDO ----------
    y_minimo = 45  # Patamar mínimo sempre = 45%
    y_meta = 100   # Meta = 100%

    if resultado < minimo:
        atingimento = 0
    else:
        m = (y_meta - y_minimo) / (y_meta - minimo)
        b = y_minimo - m * minimo
        atingimento = b + m * resultado


    if resultado < minimo:
        resultado_120 = resultado
    else: resultado_120 = (120-(y_minimo - ((y_meta - y_minimo) / (y_meta - minimo)) * minimo))/((y_meta - y_minimo) / (y_meta - minimo))
        
    resultado_120_graf = (120-(y_minimo - ((y_meta - y_minimo) / (y_meta - minimo)) * minimo))/((y_meta - y_minimo) / (y_meta - minimo))
                                                                                                
    resultado = max(0, min(resultado, resultado_120))  # limitar entre 0 e 120

    # Métrica personalizada para Resultado
    st.markdown(f"""
    <div class="metric-resultado">
        <div class="metric-label-resultado">Resultado</div>
        <div class="metric-value-resultado">{resultado:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

    atingimento = max(0, min(atingimento, 120))  # limitar entre 0 e 120
    
    # Métrica personalizada para Atingimento
    st.markdown(f"""
    <div class="metric-atingimento">
        <div class="metric-label-atingimento">Atingimento</div>
        <div class="metric-value-atingimento">{atingimento:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --------- GRÁFICO NA COLUNA DA DIREITA ----------
with col_chart:
    # --------- CURVA CORRIGIDA PARA PLOT ---------
    x_curve = np.linspace(minimo, resultado_120_graf, 50)
    y_curve = y_minimo + (y_meta - y_minimo) * (x_curve - minimo) / (100 - minimo)
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="Curva de Atingimento", line=dict(color="#666d6a")))
    fig.add_trace(go.Scatter(x=[minimo], y=[y_minimo], mode='markers', name="Patamar Mínimo (%)", marker=dict(color="#6e1632", size=8)))
    fig.add_trace(go.Scatter(x=[100], y=[100], mode='markers', name="100%", marker=dict(color="#156b6a", size=8)))
    fig.add_trace(go.Scatter(x=[resultado_120_graf], y=[120], mode='markers', name="120%", marker=dict(color="#103024", size=8)))
    fig.add_trace(go.Scatter(x=[resultado], y=[atingimento], mode='markers', name="Valor Simulado", marker=dict(color="#41d600", size=12)))

    fig.update_layout(
        xaxis_title="Resultado (%)",
        yaxis_title="Atingimento (%)",
        xaxis=dict(range=[0, 140], showgrid=False),
        yaxis=dict(range=[0, 140], showgrid=False),
        plot_bgcolor="white",
        height=500  # Ajuste a altura para melhor visualização
    )

    # Subtítulo centralizado acima do gráfico
    st.markdown('<div class="section-title"><h3>Atingimento de Meta</h3></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

# --------- FOOTER ----------
st.markdown('<div class="footer">⚠️ Este painel é uma simulação e não substitui os resultados oficiais.</div>', unsafe_allow_html=True)

# --------- LEGENDA (Inputs e Outputs) ----------
st.markdown(
    """
    <div style="margin-top:20px; padding:15px; border-radius:12px; background-color:#f5f5f5; color:#2b2d2c;">
        <h4 style="margin-bottom:10px;">📌 Legenda:</h4>
        <ul style="margin:0; padding-left:20px; line-height:2.0;">
            <li><b>Sentido do Indicador:</b> Define se o desempenho é melhor quando o valor é <i>maior</i> ou <i>menor</i>.</li>
            <li><b>Patamar Mínimo:</b> Valor mínimo necessário para iniciar o cálculo de atingimento.</li>
            <li><b>Meta:</b> Valor definido como objetivo (100%).</li>
            <li><b>Realizado:</b> Valor efetivamente alcançado.</li>
            <li><b style="background-color:#d7e1de; color:#2b2d2c; padding:3px 6px; border-radius:6px;">Resultado:</b> Percentual calculado em relação à meta (0% a 120%).</li>
            <li><b style="background-color:#2d5016; color:white; padding:3px 6px; border-radius:6px;">Atingimento:</b> Percentual ajustado que considera o patamar mínimo e a curva de atingimento.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)




