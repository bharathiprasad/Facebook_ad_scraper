#still under development

import pandas as pd
import sqlite3
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import inferno
from bokeh.transform import factor_cmap

def file_to_df(data_file): #file must be in csv format with ~ as delimiter
    import pandas as pd

    file_list = []
    headers = []
    with open(data_file, 'r') as r:
        first = True
        for line in r:
            line = line.strip().split('~')
            if first is True:
                headers = line
                first = False
            else:
                file_list.append(line)
    df = pd.DataFrame(file_list, columns=headers)
    return df

def frequency_plot(user):
    output_file('plots/frequency_plot.html')

    with sqlite3.connect('data/ad_data.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM "+user)
        rows = cur.fetchall()

    df = pd.DataFrame(columns=['ad_title'])

    for i in range(len(rows)):
        df.loc[i]=rows[i][0]
    new_df = df.groupby('ad_title')['ad_title'].describe().drop(['top','freq','unique'], axis=1)
    source = ColumnDataSource(new_df)
    ad_titles = source.data['ad_title'].tolist()

    p = figure(x_range=ad_titles)

    palette = inferno(len(rows))
    color_cmap = factor_cmap(field_name='ad_title', palette=palette, factors=ad_titles)

    p.vbar(x='ad_title', top='count', source=source, width=0.7, color=color_cmap)

    p.title.text='List of Advertisement enterprises with frequency of appearance'
    p.xaxis.axis_label='Advertisement Enterprise'
    p.yaxis.axis_label='Frequency'

    hover = HoverTool()
    hover.tooltips=[
        ("Brand", "@ad_title")
    ]
    hover.mode = 'vline'

    p.add_tools(hover)

    show(p)

def top_five_most_frequent(user):
    output_file('plots/top_five_most_frequent.html')

    with sqlite3.connect('data/ad_data.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM "+user)
        rows = cur.fetchall()

    df = pd.DataFrame(columns=['ad_title'])

    for i in range(len(rows)):
        df.loc[i]=rows[i][0]
    new_df = df.groupby('ad_title')['ad_title'].describe().drop(['top','freq','unique'], axis=1)
    new_df = new_df.sort_values('count', ascending=False).reset_index().loc[:4]

    source = ColumnDataSource(new_df)
    ad_titles = source.data['ad_title'].tolist()

    p = figure(x_range=ad_titles)

    palette = inferno(5)
    color_cmap = factor_cmap(field_name='ad_title', palette=palette, factors=ad_titles)

    p.vbar(x='ad_title', top='count', source=source, width=0.7, color=color_cmap)

    p.title.text='Top 5 in most appeared Advertisements'
    p.xaxis.axis_label='Advertisement Enterprise'
    p.yaxis.axis_label='Frequency'

    hover = HoverTool()
    hover.tooltips=[
        ("Brand", "@ad_title")
    ]
    hover.mode = 'vline'

    p.add_tools(hover)

    show(p)
