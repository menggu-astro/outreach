import matplotlib, pandas, numpy as np
import matplotlib.pyplot as plt
from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Range1d, LabelSet, Label, Arrow, OpenHead, NormalHead, VeeHead
from bokeh.plotting import figure, output_file, show, curdoc, output_notebook
from bokeh.themes import Theme
import yaml
from bokeh.server.server import Server
from bokeh.embed import components

met_allowed = [-1.1, -1.0, -0.9, -0.8, -0.7, -0.6, -0.5,
               -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2]
age_allowed = [1., 2., 3., 4., 5., 6., 7., 8., 9., 
               10., 11., 12., 13.]



allspec = []

for age, met in list(itertools.product(age_allowed, met_allowed)):
    # File names
    fname1 = 'model/cont_z' + str(round(met, 1)) + '_age' + \
        str(round(age, 1)) + '.dat'
    fname2= 'model/normcont4047_z' + str(round(met, 1)) + '_age' + \
        str(round(age, 1)) + '.dat'
    fname3 = 'model/normcont4757_z' + str(round(met, 1)) + '_age' + \
        str(round(age, 1)) + '.dat'
    fname4 = 'model/normcont5767_z' + str(round(met, 1)) + '_age' + \
        str(round(age, 1)) + '.dat'
    fname5 = 'model/normcont8089_z' + str(round(met, 1)) + '_age' + \
        str(round(age, 1)) + '.dat'
    fname6 = 'model/normcont9010_z' + str(round(met, 1)) + '_age' + \
        str(round(age, 1)) + '.dat'

    wave = pandas.read_csv(fname1)['wave'].values
    flux1 = pandas.read_csv(fname1)['flux'].values
    flux2 = pandas.read_csv(fname2)['flux'].values
    flux3 = pandas.read_csv(fname3)['flux'].values
    flux4 = pandas.read_csv(fname4)['flux'].values
    flux5 = pandas.read_csv(fname5)['flux'].values
    flux6 = pandas.read_csv(fname6)['flux'].values
    
    temdata = np.vstack((wave, flux1, flux2, 
                         flux3, flux4, flux5, flux6))
    
    allspec.append(
        {'param': 10000*int(age)+int(met*10), 'wave': wave,
         'data': temdata})
    
    
specdata = pandas.DataFrame(allspec)
spec_cds = ColumnDataSource(specdata)

# default spectrum
ind0 = spec_cds.data['param']==10000*int(1.0)+int(-1.0*10)
data0 = spec_cds.data['data'][ind0][0]

# This is the source used for plot
spec_plot = ColumnDataSource(
    data=dict(wave=data0[0], flux1=data0[1]))


s0 = figure(x_range=(3500, 1.1e4), plot_width=800, plot_height=200, title=None)
s0.xaxis.axis_label = "Wavelength"
s0.yaxis.axis_label = "Flux"
s0.line('wave', 'flux1', source=spec_plot, line_width=1, line_alpha=0.75, line_color='black')


age = Slider(title="age", value=1., start=1., end=13., step=1.)
zmet = Slider(title="[Z/H]", value=-1., start=-1.1, end=0.2, step=0.1)

