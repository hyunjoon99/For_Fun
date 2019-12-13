import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from bokeh.io import show, output_notebook, output_file, push_notebook

from bokeh.models import ColumnDataSource, HoverTool, Legend, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RadioGroup, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def demo_tab(src_csv):
    
   # Make Dataset for all States per Year
    def make_dataset(variables, year = 2000):
        src = src_csv.query('STATEID < 60 and STATEID != 52 and STATEID != 11')
        variables.append('STATE')
        src = src.loc[src['YEAR'] == year, variables]
        src = src.set_index('STATE')
        print(src)
        return ColumnDataSource(src) 
    
    # draw the plot
    def make_plot(src):
        print('make plot')
        bp = figure(plot_width = 1200, plot_height = 600,
                title = "Demographics Per State",
                x_range = src.data['STATE'],
                x_axis_label = 'State', y_axis_label = 'Number of Prisoners')

        states = src.data['STATE']
        races = list()
        colors = list()
        for i, x in enumerate(src.data):
            if x == 'index' or x == 'STATE':
                continue
            races.append(x)
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
    
    # update function
    def update(attr, old, new):
        # get list of variables to update
        print('update')
        demo_to_plot = [demo_selection.labels[i] for i in 
                            demo_selection.active]
        
        # update the slider for year
        year = year_select.value

        # update the dataset
        new_src = make_dataset(demo_to_plot, year)
        src = new_src
     
    print('update done')
    #create a checkbox
    race = ['ASIANM', 'ASIANF', 'WHITEM', 'WHITEF', 'BLACKM', 'BLACKF', 'HISPM', 'HISPF']
    demo_selection =  CheckboxGroup(labels = race, active=[0, 1, 2])
    demo_selection.on_change('active', update)

    # create a slider for year
    year_select = Slider(start = 1978, end = 2016, step = 1, value = 2001, title = 'Year')
    year_select.on_change('value', update)
    
    # Initialize the plot
    initial_active = [demo_selection.labels[i] for i in demo_selection.active]
    print(initial_active)
    print(year_select.value)
    src = make_dataset(initial_active, year_select.value)
    p = make_plot(src)
    
    # add the controls
    controls = WidgetBox(year_select, demo_selection)
    
    # create a layout
    layout = row(controls, p)
    
    # add a tab
    tab = Panel(child = layout, title = 'Prison Admissions by Ethnicity')
    
    return tab