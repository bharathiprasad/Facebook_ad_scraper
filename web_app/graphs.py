#still under development

import pandas as pd
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

def frequency_graph():

    # initialising data
    output_file('graphs/test_ad_data_plot.html')

    adf = pd.read_csv('data/test_ad_data.txt', delimiter='~')
    new_df = adf.groupby('ad_title')['ad_title'].describe()
    source = ColumnDataSource(new_df)
    ad_titles = source.data['ad_title'].tolist()

    p = figure(x_range=ad_titles)

    palette = inferno(49)
    color_cmap = factor_cmap(field_name='ad_title', palette=palette, factors=ad_titles)

    p.vbar(x='ad_title', top='count', source=source, width=0.7, color=color_cmap)

    p.title.text='List of Advertisement enterprises with frequency of appearance'
    p.xaxis.axis_label='Advertisement Enterprise'
    p.yaxis.axis_label='Frequency'

    hover = HoverTool()
    hover.tooltips=[
        ("Title", "@ad_title")
    ]
    hover.mode = 'vline'

    p.add_tools(hover)

    show(p)
