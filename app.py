''' https://community.plotly.com/t/using-buttons-as-tabs/15768/5 '''
''' https://stackoverflow.com/questions/63811550/plotly-how-to-display-graph-after-clicking-a-button '''
''' https://dash.plotly.com/dash-core-components/slider '''

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


chart_dict = {
    'FDDA1-01': 'SAT SP', 'FDDA1-02': 'SAP SP', 'FDDA1-03': 'RAT SP', 'FDDA1-04': 'RARH SP', 'FDDA1-05': 'EAP/RAP SP',
    'FDDA2-01': 'FAT/PAT', 'FDDA2-02': 'SAT', 'FDDA2-03': 'PAT', 'FDDA2-04': 'RAT', 'FDDA2-05': 'EAT',
    'FDDA2-06': 'FAPARH', 'FDDA2-07': 'SARH', 'FDDA2-08': 'RARH', 'FDDA2-09': 'EARH', 'FDDA2-10': 'PAP',
    'FDDA2-11': 'SAP', 'FDDA2-12': 'RAP', 'FDDA2-13': 'EAP', 'FDDA2-14': 'CO2',
    'FDDA3-01': 'CW Vlv Ctrl.', 'FDDA3-02': 'HW Vlv Ctrl.', 'FDDA3-03': 'VSD Speed Ctrl. SAF',
    'FDDA3-04': 'FAN On/Off Ctrl. SAF', 'FDDA3-05': 'VSD Bypass sts SAF', 'FDDA3-06': 'VSD Speed Ctrl. EAF',
    'FDDA3-07': 'FAN On/Off Ctrl. EAF', 'FDDA3-08': 'VSD Bypass sts EAF', 'FDDA3-09': 'Damper Ctrl. PA',
    'FDDA3-10': 'Damper Ctrl. FA', 'FDDA3-11': 'Damper Ctrl. RA', 'FDDA3-12': 'Damper Ctrl. EA',
    'FDDA3-13': 'Damper Ctrl. EA(PAU)', 'FDDA3-14': 'Damper Ctrl. BD', 'FDDA3-15': 'VSD Speed Ctrl. RAF',
    'FDDA3-16': 'FAN On/Off Ctrl. RAF', 'FDDA3-17': 'VSD Bypass sts RAF'}


# plotly
df_qeh = pd.read_csv(f'Data\\QEH_performance_Apr.csv')
print(df_qeh.columns)  # 'Chart Name', 'System', 'KPI'
chart_name_list = df_qeh['Chart Name'].unique()
# print(chart_name_list)

df_qeh['Chart Abbrv'] = df_qeh.apply(lambda row: chart_dict.get(row['Chart Name'], 0), axis=1)
# print(df_qeh.head(50))

chart_a1_list = ['FDDA1-01', 'FDDA1-02', 'FDDA1-03', 'FDDA1-04', 'FDDA1-05']
chart_a2_list = ['FDDA2-01', 'FDDA2-02', 'FDDA2-03', 'FDDA2-04', 'FDDA2-05', 'FDDA2-06', 'FDDA2-07', 'FDDA2-08',
                 'FDDA2-09', 'FDDA2-10', 'FDDA2-11', 'FDDA2-12', 'FDDA2-13', 'FDDA2-14']
chart_a3_list = ['FDDA3-01', 'FDDA3-02', 'FDDA3-03', 'FDDA3-04', 'FDDA3-05', 'FDDA3-06', 'FDDA3-07', 'FDDA3-08',
                 'FDDA3-09', 'FDDA3-10', 'FDDA3-11', 'FDDA3-12', 'FDDA3-13', 'FDDA3-14', 'FDDA3-15', 'FDDA3-16',
                 'FDDA3-17']


# DASH LAYOUT
app = Dash(__name__)

tabs_styles = {
    'height': '44px',
    'width': '404px',
    'padding-left': '35%', 'padding-right': '35%',
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    html.H2('QEH T-Block'),
    html.P('Chart Selection:'),
    html.Div([dcc.Tabs(id='display_figure', value='Tab 1', children=[
        dcc.Tab(label='Chart 1', value='Chart 1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Chart 2', value='Chart 2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Chart 3', value='Chart 3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Table 1', value='Table 1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Table 2', value='Table 2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Table 3', value='Table 3', style=tab_style, selected_style=tab_selected_style)]
                       )], style=tabs_styles),

    dcc.Graph(id="graph_heatmap", style={'marginLeft': '15vh', 'marginRight': '15vh'}),
    html.Div([dcc.Slider(id='slider', min=0, max=100, marks=None, step=None, value=100,
                         tooltip={"always_visible": True,
                                  "style": {"color": "LightSteelBlue", "fontSize": "14px"}}
                         )],
             style={'width': '10%', 'padding-top': '1%', 'padding-left': '45%', 'padding-right': '45%', 'textAlign': 'center'}),
])


@app.callback(
    Output("graph_heatmap", "figure"),
    Input('display_figure', 'value'),
    Input('slider', 'value'))
def plotly_heatmap(display_figure, kpi_val):
    # initial heatmap
    chart_list = chart_a1_list

    df = df_qeh.query(f'KPI <= {kpi_val}')
    df_chart = df[df['Chart Name'].isin(chart_list)]
    df_p = df_chart.pivot_table(index='System', columns='Chart Abbrv', values='KPI', aggfunc="mean").fillna(0)

    fig = go.Figure(px.imshow(df_p, aspect="auto", text_auto=".0f", color_continuous_scale="YlOrRd",
                              title="T-Block Graph"))

    fig.layout.width, fig.layout.height = 1400, 750

    # interactive selection
    if display_figure in ['Chart 1', 'Table 1']:
        chart_list = chart_a1_list
    elif display_figure in ['Chart 2', 'Table 2']:
        chart_list = chart_a2_list
    elif display_figure in ['Chart 3', 'Table 3']:
        chart_list = chart_a3_list

    df = df_qeh.query(f'KPI <= {kpi_val}')
    df_chart = df[df['Chart Name'].isin(chart_list)]
    df_p = df_chart.pivot_table(index='System', columns='Chart Abbrv', values='KPI', aggfunc="mean").fillna(0)

    if display_figure in ['Chart 1', 'Chart 2', 'Chart 3']:
        fig = go.Figure(px.imshow(df_p, aspect="auto", text_auto=".0f", color_continuous_scale="YlOrRd",
                                  title="T-Block Graph"))

        fig.layout.width, fig.layout.height = 1400, 750

    elif display_figure in ['Table 1', 'Table 2', 'Table 3']:
        # append index
        header_list = ['System'] + df_p.columns.values.tolist()
        sys_list = df_p.index.values.tolist()
        row_list = df_p.transpose().values.tolist()
        row_list.insert(0, sys_list)

        fig = go.Figure(data=[go.Table(header=dict(values=header_list),
                                       cells=dict(values=row_list))])

    return fig


if __name__ == '__main__':
    app.run(debug=True)