import pandas as pd
import plotly.graph_objs as go

config_plot = {"displaylogo": False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}

def preprocess_data(df, x_axis, y_axis, group_by=None, aggregation='count'):
    if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
        df = df.to_frame(index=False)

    # remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
    df = df.reset_index().drop('index', axis=1, errors='ignore')
    df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

    if group_by:
        chart_data = pd.concat([
            df[x_axis],
            df[y_axis],
            df[group_by],
        ], axis=1)
    else:
        chart_data = pd.concat([
            df[x_axis],
            df[y_axis],
        ], axis=1)

    aggregation_txt = (aggregation if isinstance(aggregation, str) else aggregation.__name__).capitalize()

    if group_by:
        chart_data = chart_data.sort_values([group_by, x_axis])
        chart_data = chart_data.rename(columns={x_axis: 'x'})
        chart_data = chart_data.groupby([group_by, 'x'], dropna=True)[[y_axis]].agg(aggregation)
    else:
        chart_data = chart_data.sort_values([x_axis])
        chart_data = chart_data.rename(columns={x_axis: 'x'})
        chart_data = chart_data.groupby(['x'], dropna=True)[[y_axis]].agg(aggregation)

    chart_data.columns = [f'{y_axis}||{aggregation_txt}']
    chart_data = chart_data.reset_index()
    chart_data = chart_data.dropna()

    return chart_data

def bar_chart(df, x_axis, y_axis, group_by, aggregation='count', x_label=None, y_label=None, title=None, to_html=True):
    aggregation_txt = (aggregation if isinstance(aggregation, str) else aggregation.__name__).capitalize()

    chart_data = preprocess_data(df, x_axis, y_axis, group_by, aggregation=aggregation)

    charts = []
    for it in chart_data[group_by].unique():
        print(it)
        chart_data_tmp = chart_data.query(f"`{group_by}` == '{it}'")
        charts.append(go.Bar(
            x=chart_data_tmp['x'],
            y=chart_data_tmp[f'{y_axis}||{aggregation_txt}'],
            name=f'({group_by}: {it})'
        ))

    figure = go.Figure(data=charts, layout=go.Layout({
        'barmode': 'group',
        'legend': {'orientation': 'h', 'y': -0.3},
        'title': {'text': title or f'{aggregation_txt} of {y_axis} by {x_axis}'},
        'xaxis': {'title': {'text': x_label or x_axis}},
        'yaxis': {'tickformat': '0:g', 'title': {'text': y_label or f'{aggregation_txt} of {y_axis}'}, 'type': 'linear'}
    }))

    if to_html:
        return figure.to_html(full_html=False, config=config_plot)
    return figure

def pie_chart(df, x_axis, y_axis, aggregation='count', x_label=None, y_label=None, title=None, to_html=True):
    aggregation_txt = (aggregation if isinstance(aggregation, str) else aggregation.__name__).capitalize()

    chart_data = preprocess_data(df, x_axis, y_axis, aggregation=aggregation)
    chart_data = chart_data[chart_data[f'{y_axis}||{aggregation_txt}'] > 0]  # can't represent negatives in a pie

    chart = go.Pie(labels=chart_data['x'], values=chart_data[f'{y_axis}||{aggregation_txt}'])
    figure = go.Figure(data=[chart], layout=go.Layout({
        'legend': {'orientation': 'h', 'y': -0.3}, 'title': {'text': title or f'{aggregation_txt} of {y_axis} by {x_axis}'}
    }))

    if to_html:
        return figure.to_html(full_html=False, config=config_plot)
    return figure

def line_chart(df, x_axis, y_axis, aggregation='count', x_label=None, y_label=None, title=None, to_html=True):
    aggregation_txt = (aggregation if isinstance(aggregation, str) else aggregation.__name__).capitalize()
    
    chart_data = preprocess_data(df, x_axis, y_axis, aggregation=aggregation)

    charts = []
    line_cfg = {'line': {'shape': 'spline', 'smoothing': 0.3}, 'mode': 'lines'}
    charts.append(go.Scatter(
        x=chart_data['x'], y=chart_data[f'{y_axis}||{aggregation_txt}'], name=f'({y_axis}||{aggregation_txt})', **line_cfg
    ))
    figure = go.Figure(data=charts, layout=go.Layout({
        'legend': {'orientation': 'h', 'y': -0.3},
        'title': {'text': title or f'{aggregation_txt} of {y_axis} by {x_axis}'},
        'xaxis': {'title': {'text': x_label or x_axis}},
        'yaxis': {'title': {'text': y_label or f'{aggregation_txt} of {y_axis}'}, 'type': 'linear'}
    }))

    if to_html:
        return figure.to_html(full_html=False, config=config_plot)
    return figure
