import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from bokeh.io import show, output_notebook, output_file, push_notebook

from bokeh.models import ColumnDataSource, HoverTool, Legend, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RadioGroup, Tabs, RadioButtonGroup

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def sentence_tab(src_csv):
    
   # Make Dataset for all States per Year
    def make_dataset():
        new_src = src_csv.loc[src_csv['STATEID'] == 99, ['YEAR', 'JURGT1M', 'JURLT1M', 'JURGT1F', 'JURLT1F']]
        return ColumnDataSource(new_src) 
    
    # draw the plot
    def make_plot(sentenceL):
        l = figure(plot_width = 800, plot_height = 600,
            title = "Received Sentence Lengths",
              x_axis_label = 'Year', y_axis_label = 'Number of Prisoners')


        l1 = l.circle(sentenceL.data['YEAR'], sentenceL.data['JURGT1M'],
                 size = 7, color = 'navy', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'navy')

        l2 = l.circle(sentenceL.data['YEAR'], sentenceL.data['JURLT1M'],
                 size = 7, color = 'red', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'red')

        l3 = l.circle(sentenceL.data['YEAR'], sentenceL.data['JURGT1F'],
                 size = 7, color = 'green', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'green')

        l4 = l.circle(sentenceL.data['YEAR'], sentenceL.data['JURLT1F'],
                 size = 7, color = 'purple', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'purple')


        # adding tooltips
        h = HoverTool(tooltips = [
            ('Year', '@x'),
            ('# of Prisoners', '@y')
            ])

        l.add_tools(h)

        # Legend
        legendl = Legend(items=[
            ('Male, More than 1 Year', [l1]),
            ('Male, Less than Year', [l2]),
            ('Female, More than 1 Year', [l3]),
            ('Female, Less than 1 Year', [l4])
        ])

        l.add_layout(legendl, 'right')
        l.legend.click_policy='hide'

        return l
    
 
    
    src = make_dataset()
    p = make_plot(src)

    # create a layout
    layout = row(p)
    
    # add a tab
    tab = Panel(child = layout, title = 'Sentence Lengths')
    return tab