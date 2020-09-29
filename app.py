import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import flask
from dash.dependencies import Input, Output, State
from scipy.stats import gaussian_kde

# Tutorial: https://dash.plotly.com/layout

################################
# 0. colors
################################

grey = '#f7f4eb'
teal = '#3C7A89'
purple = '#37123C'
rose = '#945D5E'

################################
# 1. Data
################################

df = pd.read_csv('income_data.csv')
kernel_original = gaussian_kde(df.income, weights=df.weights)
# generate equally spaced X values
xs = np.linspace(min(df.income), max(df.income), 1000)
dist_original = kernel_original(xs)

################################
# 2. App Layout
################################

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[

    html.Header(
        html.H1(children='Efectos en pobreza y desigualdad '
                                          'del Covid-19'),
        style={'color':'#945D5E'}
    ),

    html.P(
        children= u"Esta aplicación visualiza de forma interactiva los "
                  u"efectos en la distribucuión del ingreso de posibles "
                  u"choques a algunos sectores productivos. Por el momento, "
                  u"los datos son simulados."
                u" Para empezar a interactuar con la aplicación, seleccione "
                  u"los sectores que recibirán un choque e "
                 u"introduzca el porcentaje de los ingresos originales "
                 u"que recibirán. Por ejemplo, al seleccionar el sector "
                 u" 'transporte' e introducir 60%, se reducirán los "
                 u"ingresos de todas las personas pertenecientes a este "
                 u"sector al 60% de sus ingresos originales. Al "
                 u"finalizar, el botón de 'aplicar' actualizará la "
                 u"gráfica."),
    html.Hr(),


    #-------------------------
    # user input
    #-------------------------
    html.Div(
        className='three columns',
        children=[

        # Sector-Shock pair (1)
        html.Div([
            html.Div([
                dcc.Checklist(
                    id='sector1',
                    options=[
                        {'label': 'Transporte', 'value': 1}
                    ],
                )], style={'font-size': '1em', 'color':'#945D5E'}),

            html.Div([
                dcc.Input(
                    id='shock1',
                    type='number',
                    min=0,
                    step=1,
                    max=100,
                    value=100
                )], style={'marginBottom': '2em'}),

        ]),

        # Sector-Shock pair (2)
        html.Div([
            html.Div([
                dcc.Checklist(
                    id='sector2',
                    options=[
                        {'label': u'Construcción', 'value': 2}
                    ],
                )], style={'font-size': '1em', 'color':'#945D5E'}),

            html.Div([
                dcc.Input(
                    id='shock2',
                    type='number',
                    min=0,
                    max=100,
                    step=1,
                    value=100
                )], style={'marginBottom': '2em'})
        ]),

        # Sector-Shock pair (3)
        html.Div([
            html.Div([
                dcc.Checklist(
                    id='sector3',
                    options=[
                        {'label': 'Manufactura', 'value': 3}
                    ],
                )], style={'font-size': '1em', 'color':'#945D5E'}),

            html.Div([
                dcc.Input(
                    id='shock3',
                    type='number',
                    min=0,
                    max=100,
                    step=1,
                    value=100
                )], style={'marginBottom': '3em'})
        ]),

        # button at the end
        html.Button(id='apply-button', n_clicks=0, children='Aplicar',
                    style={'background-color': rose,
                           'color': 'white'})
        ]),

    # -------------------------
    # plot
    # -------------------------
    html.Div(
        className= 'eight columns',
        children=[
        # select reference lines
        dcc.Checklist(
            id='reference-lines',
            options=[
                {'label': u'Salario Mínimo -',
                 'value': 'Minimum Wage'},
                {'label': u'Línea de Pobreza -',
                 'value': 'Poverty Line'},
                {'label': u'Línea de Vulnerabilidad -',
                 'value': 'Vulnerability Line'}
            ],
            labelStyle={'display': 'inline-block'},
            style={'background-color': 'white'}
            ),
        dcc.Graph(id='histogram')
        ])

], className='row', style={'background-color': 'white'})


################################
# 3. App Callbacks
################################

@app.callback(
    Output('histogram', 'figure'),
    [Input('apply-button', 'n_clicks'),
     Input('reference-lines', 'value')],
    [State('sector1', 'value'),
     State('sector2', 'value'),
     State('sector3', 'value'),
     State('shock1', 'value'),
     State('shock2', 'value'),
     State('shock3', 'value')]
)
def update_figre(n_clicks,
                 reference_lines,
                 sector1, sector2, sector3,
                 shock1, shock2, shock3):
    df_shock = df.copy()
    selected_sectors = [sector1, sector2, sector3]

    for sector in selected_sectors:
        if sector is not None and sector:
            sector = sector[0]
            if sector == 1:
                df_shock.loc[df_shock['sector'] == sector, 'income'] = \
                    df_shock[
                        'income'] * (shock1 / 100)
                continue

            if sector == 2:
                df_shock.loc[df_shock['sector'] == sector, 'income'] = df_shock[
                                                                           'income'] * (
                                                                                   shock2 / 100)
                continue

            if sector == 3:
                df_shock.loc[df_shock['sector'] == sector, 'income'] = df_shock[
                                                                           'income'] * (
                                                                                   shock3 / 100)
                continue

    # Option 1: No weights
    # https://plotly.com/python/distplot/
    # hist_data = [df_shock.income]
    # group_labels = ['distplot']
    # fig = ff.create_distplot(hist_data, group_labels,
    #                          curve_type='kde',
    #                          show_hist=False,
    #                          show_rug=True, # show box below
    #                          colors=[selected_color])

    # Option 2: Weights
    # compute kernel
    kernel_shock = gaussian_kde(df_shock.income, weights=df_shock.weights)

    # Create traces
    # https://plotly.com/python/line-charts/
    fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text=u"Distribución del ingreso, pobreza y "
                                   u"vulnerabilidad"),
        xaxis=go.layout.XAxis(title="Ingreso (en miles de pesos)"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='grey')
    )

    # modified distribution
    fig.add_trace(go.Scatter(x=xs, y=kernel_shock(xs),
                             mode='lines',
                             name=u'Distribución Modificada',
                             line=dict(color='#DDA77B')))

    # Original distribution
    fig.add_trace(go.Scatter(x=xs, y=dist_original,
                             mode='lines',
                             name=u'Distribución Original',
                             line=dict(color='#37123C')))


    lines = []

    if reference_lines is not None:
        if 'Minimum Wage' in reference_lines:
            fig.add_trace(go.Scatter(
                x=[700+40],
                y=[0.0005],
                text=u'Salario<br>Mínimo',
                mode="text",
                showlegend=False,
                textfont={'color': 'red'}
            ))

            MW = dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=700, x1=700,
                line=dict(
                    color="red",
                    width=2,
                    dash="dashdot"
                )
            )
            # save dictionary to list
            lines.append(MW)

        if 'Poverty Line' in reference_lines:
            fig.add_trace(go.Scatter(
                x=[200+50],
                y=[max(dist_original)],
                text=u'Línea de<br>pobreza',
                mode="text",
                showlegend=False,
                textfont={'color': teal}
            ))

            PL = dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=200, x1=200,
                line=dict(
                    color=teal,
                    width=2,
                    dash="dashdot"
                )
            )
            # save dictionary to list
            lines.append(PL)

        if 'Vulnerability Line' in reference_lines:
            fig.add_trace(go.Scatter(
                x=[450+65],
                y=[max(dist_original)],
                text=u'Línea de<br>vulnerabilidad',
                mode="text",
                showlegend=False,
                textfont={'color': "#c79408"}
            ))

            VL = dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=450, x1=450,
                line=dict(
                    color="#c79408",
                    width=2,
                    dash="dashdot"
                )
            )
            # save dictionary to list
            lines.append(VL)

        fig.update_layout(shapes=lines)

    return fig

################################
# 4. Run App
################################

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
