import pandas as pd
import numpy as np
from os.path import dirname, join

from bokeh.io import curdoc, show, output_notebook
from bokeh.models.widgets import Tabs


# Import Graphs
from scripts.demo import demo_tab
from scripts.release import release_tab
from scripts.sentence import sentence_tab

from bokeh.sampledata.us_states import data as states


# read data from CSV
#NPS = pd.read_csv('bokeh_app/data/NPS.tsv', na_values=['-9', '-2', '-1', '-8'], sep='\t')
NPS = pd.read_csv(join(dirname('__file__'), 'bokeh_app', 'data', 'NPS.tsv'), na_values=['-9', '-2', '-1', '-8'], sep='\t')

# Draw Tabs
tab1 = demo_tab(NPS, 2000)
tab2 = demo_tab(NPS, 2005)
tab3 = demo_tab(NPS, 2010)
tab4 = demo_tab(NPS, 2015)

tab5 = release_tab(NPS)

tab6 = sentence_tab(NPS)

tabs = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5, tab6])
curdoc().add_root(tabs)