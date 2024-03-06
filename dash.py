# Importa as bibliotecas necessárias
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Função para processar os dados
def process_data(df):
    all_nodes = set()
    source_target_weights = {}

    for _, row in df.iterrows():
        connections = row['connections'].split('->')
        weight = row['totals']

        for i, course in enumerate(connections):
            all_nodes.add((course, i))
            if i < len(connections) - 1:
                source = (course, i)
                target = (connections[i+1], i+1)
                key = (source, target)
                if key in source_target_weights:
                    source_target_weights[key] += weight
                else:
                    source_target_weights[key] = weight

    consolidated_source_target_weights = [(source, target, weight) for (source, target), weight in source_target_weights.items()]
    return all_nodes, consolidated_source_target_weights

# Carrega os dados
@st.cache_data  # Atualizado para usar cache_data
def load_data():
    # df = pd.read_csv('students_connections_2.csv')
    df = pd.read_csv('https://metabase.k21.com.br/public/question/ca0b837e-d3d8-4b0a-b3fb-db03ff2ed0f8.csv')
    return df

df = load_data()
all_nodes, source_target_weights = process_data(df)

# Mapeando os nós para índices numéricos
node_list = list(all_nodes)
node_indices = {node: i for i, node in enumerate(node_list)}

# Criando listas de source, target e value
sources = [node_indices[source] for source, target, weight in source_target_weights]
targets = [node_indices[target] for source, target, weight in source_target_weights]
values = [weight for source, target, weight in source_target_weights]

# Definindo as cores
# Lista com cores para os treinamentos
cores_treinamentos = {
    'FLSA': '#4682B4',  # SteelBlue
    'KSD': '#008B8B',   # DarkCyan
    'Facilitação': '#DAA520',  # Goldenrod
    'Métricas': '#708090',  # SlateGray
    'MGT3.0': '#FF4500',  # OrangeRed
    'CSPO': '#6A5ACD',  # SlateBlue
    'ACPO': '#20B2AA',  # LightSeaGreen
    'OKR': '#2E8B57',   # SeaGreen
    'CSM': '#778899',   # LightSlateGray
    'F4P': '#9932CC',   # DarkOrchid
    'ACSM': '#BDB76B',  # DarkKhaki
    'KSI': '#FFD700',   # Gold
    'RHAgil': '#E9967A',  # DarkSalmon
    'OutrosEventosOuTreinamentos': '#DCDCDC',  # Gainsboro
    'TKP': '#7CFC00',   # LawnGreen
    'KMM': '#FA8072',   # Salmon
    'Combo KMM+KCP': '#DB7093',  # PaleVioletRed
    'Combo KSD+KSI': '#4169E1',  # RoyalBlue
    'KCP': '#8FBC8F',  # DarkSeaGreen
    'FL2D': '#B22222',  # FireBrick
    'KSD+MET': '#FF69B4',  # HotPink
    'Comunicação': '#4B0082',  # Indigo
    'Retrospectivas': '#ADD8E6',  # LightBlue
    'MétricasGProdutos': '#F08080',  # LightCoral
    'KDI': '#9370DB',  # MediumPurple
    'WGN por Métricas': '#3CB371',  # MediumSeaGreen
    'DesignThinking': '#C71585',  # MediumVioletRed
    'OKR PRO': '#FFA500',  # Orange
    'WS Estimativas': '#87CEFA',  # LightSkyBlue
}

# Criando labels e cores para os nós
labels = [f'{node[0]}' for node in node_list]
colors = [cores_treinamentos.get(node[0], '#FFFFFF') for node in node_list]

# Criando o diagrama de Sankey com Plotly
fig = go.Figure(data=[go.Sankey(
    arrangement='snap',
    valueformat = '.0f',
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.2),
        label=labels,
        color=colors,  # Assegurando que as cores sejam aplicadas corretamente
        align='left',
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
    ))])

# Configurações do layout do diagrama, ajustando as margens
fig.update_layout(
    title_text="K21 - Trilhas Executadas",
    font_size=15,
    height=980,  # Pode ajustar se necessário
    width=1000,  # Largura ajustada para caber melhor na tela
    margin=dict(l=0, r=0, t=0, b=0)  # Ajusta as margens aqui
)

# Mostra o diagrama de Sankey no Streamlit
st.plotly_chart(fig, use_container_width=True)
