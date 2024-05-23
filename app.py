''' https://community.plotly.com/t/using-buttons-as-tabs/15768/5 '''
''' https://stackoverflow.com/questions/63811550/plotly-how-to-display-graph-after-clicking-a-button '''
''' https://dash.plotly.com/dash-core-components/slider '''


import json
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
# from datetime import datetime, timedelta


def create_chart_list():
    list_a1 = ['FDDA1-01', 'FDDA1-02', 'FDDA1-03', 'FDDA1-04', 'FDDA1-05']
    list_a2 = ['FDDA2-01', 'FDDA2-02', 'FDDA2-03', 'FDDA2-04', 'FDDA2-05', 'FDDA2-06', 'FDDA2-07', 'FDDA2-08',
               'FDDA2-09', 'FDDA2-10', 'FDDA2-11', 'FDDA2-12', 'FDDA2-13', 'FDDA2-14']
    list_a3 = ['FDDA3-01', 'FDDA3-02', 'FDDA3-03', 'FDDA3-04', 'FDDA3-05', 'FDDA3-06', 'FDDA3-07', 'FDDA3-08',
               'FDDA3-09', 'FDDA3-10', 'FDDA3-11', 'FDDA3-12', 'FDDA3-13', 'FDDA3-14', 'FDDA3-15', 'FDDA3-16',
               'FDDA3-17']

    return list_a1, list_a2, list_a3


# def date_info():
#     today = datetime.today().date()
#     first = today.replace(day=1)
#     last_mth = first - timedelta(days=1)
#     last_mth_str = last_mth.strftime("%b")
#
#     return today, last_mth_str


# load json
def load_json_file():
    # today, last_mth_str = date_info()
    # f = open(f'Data\\QEH_performance_{last_mth_str}.json')
    f = open(f'Data\\QEH_performance.json')
    json_data = json.load(f)
    # print(json_data)

    filtered = [d[1] for d in [x[1] for x in json_data.items()][2].items() if d[1] <= 80]
    # print(filtered)  # ['Chart Name', 'System', 'KPI', 'Chart Abbrv']

    # convert json to diff lists
    col_name = [key for key, val in json_data.items()]
    chart_name_val = [val for key, val in json_data['Chart Name'].items()]
    system_val = [val for key, val in json_data['System'].items()]
    kpi_val = [val for key, val in json_data['KPI'].items()]
    chart_abbrv_val = [val for key, val in json_data['Chart Abbrv'].items()]

    return col_name, chart_name_val, system_val, kpi_val, chart_abbrv_val


# to cater this code: df = df_qeh.query(f'KPI <= {kpi_val}')
def trim_list_by_kpi(kpi_v):
    col_name, chart_name_val, system_val, kpi_val, chart_abbrv_val = load_json_file()

    # extract idx list that match criteria
    idx_list = [idx for idx, ele in enumerate(kpi_val) if ele <= kpi_v]
    # print(len(idx_list), idx_list)

    chart_name_val_list = [chart_name_val[i] for i in idx_list]
    system_val_list = [system_val[i] for i in idx_list]
    kpi_val_list = [kpi_val[i] for i in idx_list]
    chart_abbrv_val_list = [chart_abbrv_val[i] for i in idx_list]

    return chart_name_val_list, system_val_list, kpi_val_list, chart_abbrv_val_list


# to cater this code: df_chart = df[df['Chart Name'].isin(chart_list)]
def trim_list_by_chart_list(chart_list, kpi_v):
    chart_name_val_list, system_val_list, kpi_val_list, chart_abbrv_val_list = trim_list_by_kpi(kpi_v=kpi_v)

    # extract idx list that match criteria
    idx_list = [idx for idx, ele in enumerate(chart_name_val_list) if ele in chart_list]
    # print(len(idx_list), idx_list)

    chart_name_val_list2 = [chart_name_val_list[i] for i in idx_list]
    system_val_list2 = [system_val_list[i] for i in idx_list]
    kpi_val_list2 = [kpi_val_list[i] for i in idx_list]
    chart_abbrv_val_list2 = [chart_abbrv_val_list[i] for i in idx_list]

    return chart_name_val_list2, system_val_list2, kpi_val_list2, chart_abbrv_val_list2


# to cater this code: df_p = df_chart.pivot_table(index='System', columns='Chart Abbrv', values='KPI', aggfunc="mean").fillna(0)
def pivot_table_no_pandas(chart_list, kpi_v):
    # below list should be fixed in later step
    chart_name_val_list2, system_val_list2, kpi_val_list2, chart_abbrv_val_list2 = trim_list_by_chart_list(chart_list=chart_list, kpi_v=kpi_v)
    # print('*'*80)
    # print(chart_name_val_list2)
    # print(system_val_list2)
    # print(kpi_val_list2)
    # print(chart_abbrv_val_list2)
    # print('*'*80)

    uni_col_list = list(set(chart_abbrv_val_list2))
    uni_row_list = list(set(system_val_list2))
    # print(uni_col_list)
    # print(uni_row_list)
    # print('*'*80)

    master_list = []
    for i, j, k in zip(chart_abbrv_val_list2, system_val_list2, kpi_val_list2):
        master_list.append([i, j, k])

    # sort 1st, then 2nd
    master_list = sorted(master_list, key=lambda x: (x[0], x[1]), reverse=True)
    # for m_list in master_list:
    #     print(m_list)
    # print('*'*80)

    # create missing row records
    master_list2 = []
    for row_item in uni_row_list:
        avail_list = []
        for m_list in master_list:
            if row_item in m_list:
                # print(row_item, m_list)
                avail_list.append(m_list[0])
                master_list2.append(m_list)
        # print(len(avail_list), avail_list)
        not_avail_list = list(set(uni_col_list) - set(avail_list))
        # print(len(not_avail_list), not_avail_list)
        for not_avail in not_avail_list:
            new_m_list = [not_avail, row_item, 0]
            # print(row_item, new_m_list)
            master_list2.append(new_m_list)
    # print('*'*80)

    # sort 2nd, then 1st
    master_list2 = sorted(master_list2, key=lambda x: (x[1], x[0]), reverse=True)
    # for master2 in master_list2:
    #     print(master2)
    # print('*'*80)

    col_list = [sublist[0] for sublist in master_list2]
    # get index of 2nd repeated item
    idx_val = [idx for idx, ele in enumerate(col_list) if ele == col_list[0]][1]
    # print(idx_val)
    col_list = col_list[0:idx_val]
    # print(len(col_list), col_list)

    row_list = [sublist[1] for sublist in master_list2]
    # get every item with step according to the len of col_list
    row_list = row_list[::idx_val]
    # print(len(row_list), row_list)

    val_list = [sublist[-1] for sublist in master_list2]
    # print(len(val_list), val_list)

    nested_val_list = [val_list[i:i+len(uni_col_list)] for i in range(0, len(val_list), len(uni_col_list))]
    # for nested_val in nested_val_list:
    #     print(nested_val, sum(nested_val))
    # print('*'*80)

    return col_list, row_list, nested_val_list

# for testing #
# chart_a1_list, chart_a2_list, chart_a3_list = create_chart_list()
# chart_list = chart_a1_list
# col_list, row_list, df_p = pivot_table_no_pandas(chart_list=chart_list, kpi_v=100)


# plotly
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
def plotly_heatmap(display_figure, kpi_v):
    chart_a1_list, chart_a2_list, chart_a3_list = create_chart_list()

    # initial heatmap
    chart_list = chart_a1_list
    col_list, row_list, df_p = pivot_table_no_pandas(chart_list=chart_list, kpi_v=kpi_v)

    ''' https://plotly.com/python/builtin-colorscales/ '''
    fig = go.Figure(px.imshow(df_p, aspect="auto", text_auto=".0f", color_continuous_scale="pinkyl",
                              title="T-Block Graph", x=col_list, y=row_list))

    fig.layout.width, fig.layout.height = 1400, 750

    # interactive selection
    if display_figure in ['Chart 1', 'Table 1']:
        chart_list = chart_a1_list
    elif display_figure in ['Chart 2', 'Table 2']:
        chart_list = chart_a2_list
    elif display_figure in ['Chart 3', 'Table 3']:
        chart_list = chart_a3_list

    col_list, row_list, df_p = pivot_table_no_pandas(chart_list=chart_list, kpi_v=kpi_v)

    if display_figure in ['Chart 1', 'Chart 2', 'Chart 3']:
        fig = go.Figure(px.imshow(df_p, aspect="auto", text_auto=".0f", color_continuous_scale="pinkyl",
                                  title="T-Block Graph", x=col_list, y=row_list))

        fig.layout.width, fig.layout.height = 1400, 750

    elif display_figure in ['Table 1', 'Table 2', 'Table 3']:
        # append index
        theader_list = ['System'] + col_list

        nrow = len(df_p)
        # 1st: change to flat list
        flat_list = [ele for sublist in df_p for ele in sublist]
        # print(flat_list)
        # 2nd: reshape to nested list
        trow_list = [flat_list[i:i + nrow] for i in range(0, len(flat_list), nrow)]
        # for trow_val in trow_list:
        #     print(trow_val, sum(trow_val))
        # print('*' * 80)
        trow_list.insert(0, row_list)

        fig = go.Figure(data=[go.Table(header=dict(values=theader_list),
                                       cells=dict(values=trow_list))])

    return fig


if __name__ == '__main__':
    app.run(debug=True)