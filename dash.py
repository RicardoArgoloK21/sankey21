# Importações necessárias
import dash
# from dash import dcc, html
from dash.dependencies import Input, Output
from dash import Dash, html, dcc, callback, Output, Input
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

# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# Define o layout do aplicativo
app.layout = html.Div([
    dcc.Graph(id='sankey-diagram'),
    html.Button('Atualizar Dados', id='update-button', n_clicks=0)
])

# Callback para atualizar o gráfico Sankey
@app.callback(
    Output('sankey-diagram', 'figure'),
    [Input('update-button', 'n_clicks')]
)
def update_sankey(n_clicks):
    df = pd.read_csv('https://metabase.k21.com.br/public/question/ca0b837e-d3d8-4b0a-b3fb-db03ff2ed0f8.csv')
    all_nodes, source_target_weights = process_data(df)
    
    # Mapeando os nós para índices numéricos
    node_list = list(all_nodes)
    node_indices = {node: i for i, node in enumerate(node_list)}

    # Criando listas de source, target e value
    sources = [node_indices[source] for source, target, weight in source_target_weights]
    targets = [node_indices[target] for source, target, weight in source_target_weights]
    values = [weight for source, target, weight in source_target_weights]

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
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=labels,
            color=colors,
            align='left',
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color='rgba(0,0,0,0.2)'
        )
    )])

    # Configurações do layout do diagrama
    fig.update_layout(
        title_text="K21 - Trilhas Executadas",
        font_size=12,
        height=900,
    )
    
    return fig

# Roda o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
