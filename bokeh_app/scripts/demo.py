import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from bokeh.io import show, output_notebook, output_file, push_notebook

from bokeh.models import ColumnDataSource, HoverTool, Legend, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RadioGroup, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def demo_tab(src_csv, year):
    
   # Make Dataset for all States per Year
    def make_dataset(year):
        src = src_csv.query('STATEID < 60 and STATEID != 52 and STATEID != 11')
        variables = ['ASIANM', 'ASIANF', 'WHITEM', 'WHITEF', 'BLACKM', 'BLACKF', 'HISPM', 'HISPF']
        variables.append('STATE')
        src = src.loc[src['YEAR'] == year, variables]
        src = src.set_index('STATE')
        return ColumnDataSource(src) 
    
    # draw the plot
    def make_plot(src):
        bp = figure(plot_width = 1200, plot_height = 600,
                title = "Demographics Per State: " + str(year),
                x_range = src.data['STATE'],
                x_axis_label = 'State', y_axis_label = 'Number of Prisoners')

        states = src.data['STATE']
        races = ['ASIANM', 'ASIANF', 'WHITEM', 'WHITEF', 'BLACKM', 'BLACKF', 'HISPM', 'HISPF']
        colors = list()
        for i, x in enumerate(src.data):
            if x == 'index' or x == 'STATE':
                continue
            colors.append(Category20_16[i])

        races_legend = list()
        for name in races:
            if name == 'ASIANM':
                races_legend.append('Asian, Male') 
            elif name == 'ASIANF':
                races_legend.append('Asian, Female')
            elif name == 'WHITEF':
                races_legend.append('White, Female')
            elif name == 'WHITEM':
                races_legend.append('White, Male')
            elif name == 'BLACKF':
                races_legend.append('Black, Female')
            elif name == 'BLACKM':
                races_legend.append('Black, Male')
            elif name == 'HISPM':
                races_legend.append('Hispanic/Latino, Male')
            elif name == 'HISPF':
                races_legend.append('Hispanic/Latino, Female')

        AM = bp.vbar_stack(races, x = 'STATE', width = 0.9, color = colors, source = src,
                           legend = races_legend)
        
        for race in races:
            h = HoverTool(tooltips = [
            ('State', '@STATE'),
            ('# of Prisoners', '@races')
            ], names = races)

            bp.add_tools(h)

        bp.legend.location = 'top_right'
        bp.legend.click_policy='hide'
    
        return bp
    
    
    # create a layout
    src = make_dataset(year)
    p = make_plot(src)
    layout = row(p)
    
    # add a tab
    tab = Panel(child = layout, title = 'Demographics:' + str(year))
    
    return tab