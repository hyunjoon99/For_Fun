import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from bokeh.io import show, output_notebook, output_file, push_notebook

from bokeh.models import ColumnDataSource, HoverTool, Legend, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RadioGroup, Tabs, RadioButtonGroup

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def release_tab(src_csv):
    
   # Make Dataset for all States per Year
    def make_dataset():
        new_src = src_csv.query('STATEID == 99 and YEAR >= 1983')
        return ColumnDataSource(new_src) 
    
    # draw the plot
    def make_plot(src):
        print('draw plot')
        m = figure(plot_width = 800, plot_height = 600,
            title = "National Prisoner Release Statistics",
              x_axis_label = 'Year', y_axis_label = 'Number of Prisoners')

        # Male
        # RLUNEXPM: UNCONDITIONAL RELEASE EXPIRATIONS OF SENTENCE, MALE
        rm = m.circle(src.data['YEAR'], src.data['RLUNEXPM'],
                 size = 7, color = 'navy', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'navy')

        # RLCOSUPM: SUPERVISED MANDATORY RELEASE, MALE
        sm = m.circle(src.data['YEAR'], src.data['RLCOSUPM'],
                 size = 7, color = 'red', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'red')

        # RLCODPM: DISCRETIONARY PAROLE, MALE
        pm = m.circle(src.data['YEAR'], src.data['RLCODPM'],
                 size = 7, color = 'green', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'green')

        # Female
        # RLUNEXPM: UNCONDITIONAL RELEASE EXPIRATIONS OF SENTENCE, FEMALE
        rf = m.square(src.data['YEAR'], src.data['RLUNEXPF'],
                 size = 7, color = 'navy', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'navy')

        # RLCOSUPM: SUPERVISED MANDATORY RELEASE, FEMALE
        sf = m.square(src.data['YEAR'], src.data['RLCOSUPF'],
                 size = 7, color = 'red', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'red')

        # RLCODPM: DISCRETIONARY PAROLE, FEMALE
        pf = m.square(src.data['YEAR'], src.data['RLCODPF'],
                 size = 7, color = 'green', alpha = 0.5,
                 hover_fill_alpha = 1.0, hover_fill_color = 'green')

        # adding tooltips
        h = HoverTool(tooltips = [
            ('Year', '@x'),
            ('# of Prisoners', '@y')
            ])

        m.add_tools(h)

        # Legend
        legendm = Legend(items=[
            ('Male, Unconditional Release', [rm]),
            ('Male, Supervised Release', [sm]),
            ('Male, Parole', [pm]),
            ('Female, Unconditional Release', [rf]),
            ('Female, Supervised Release', [sf]),
            ('Female, Parole', [pf])
        ])

        m.add_layout(legendm, 'right')
        m.legend.click_policy='hide'

        return m
    
 
    
    src = make_dataset()
    p = make_plot(src)

    # create a layout
    layout = row(p)
    
    # add a tab
    tab = Panel(child = layout, title = 'Prison Releases')
    return tab