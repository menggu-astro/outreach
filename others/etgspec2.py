from __future__ import print_function
import matplotlib, pandas, numpy as np
import matplotlib.pyplot as plt
from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import figure, output_file, show, curdoc, output_notebook
from bokeh.themes import Theme
import yaml
from bokeh.server.server import Server
from bokeh.embed import components


Spectra = {}    
for zmet in [-1.1, -1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2]:
    for age in [1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13.]:
        fname = 'model/cont_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname1 = 'model/normcont4047_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname2 = 'model/normcont4757_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname3 = 'model/normcont5767_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname4 = 'model/normcont8089_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname5 = 'model/normcont9010_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        Spectra[(int(zmet*10),(age))]=np.vstack((pandas.read_csv(fname)['wave'], pandas.read_csv(fname)['flux'], 
                                                 pandas.read_csv(fname1)['flux'], pandas.read_csv(fname2)['flux'], 
                                                 pandas.read_csv(fname3)['flux'], pandas.read_csv(fname4)['flux'], 
                                                 pandas.read_csv(fname5)['flux']))
                                                 



f0 = Spectra[(int(-1.*10), int(1.))]  
source = ColumnDataSource(data=dict(x=f0[0], y0=f0[1], y1=f0[2], y2=f0[3], y3=f0[4], y4=f0[5], y5=f0[6]))

s0 = figure(x_range=(3500, 1e4), plot_width=800, plot_height=200, title=None)
s1 = figure(x_range=(4e3, 4.7e3), y_range=(0.6, 1.2), plot_width=250, plot_height=200, title=None)
s2 = figure(x_range=(4.7e3, 5.7e3), y_range=(0.6, 1.2), plot_width=250, plot_height=200, title=None)
s3 = figure(x_range=(5.7e3, 6.7e3), y_range=(0.6, 1.2), plot_width=250, plot_height=200, title=None)
s4 = figure(x_range=(8e3, 8.92e3), y_range=(0.75, 1.15), plot_width=390, plot_height=200, title=None)
s5 = figure(x_range=(9e3, 1.01e4), y_range=(0.85, 1.1), plot_width=390, plot_height=200, title=None)
for i, tem in enumerate([s0, s1, s2, s3, s4, s5]):
        tem.xaxis.axis_label = "Wavelength"
        tem.yaxis.axis_label = "Flux"
        tem.line('x', 'y'+str(i), source=source, line_width=1, line_alpha=0.75, line_color='black')

age = Slider(title="age", value=1., start=1., end=13., step=1.)
zmet = Slider(title="[Z/H]", value=-1., start=-1.1, end=0.2, step=0.1)

def callback(attrname, old, new):
        tage = age.value
        zh = zmet.value
        fx = Spectra[(int(zh*10), int(tage))]
        source.data = dict(x=fx[0], y0=fx[1], y1=fx[2], y2=fx[3], y3=fx[4], y4=fx[5], y5=fx[6])
        
for w in [age, zmet]:
        w.on_change('value', callback)

layout = column(
        widgetbox(age, zmet),
        s0, row(s1, s2, s3), row(s4, s5))

curdoc().add_root(layout)
    
script, div = components(layout)
with open('script_etgspec.txt', 'w') as f:
        print(script, file=f)
with open('div_etgspec.txt', 'w') as f:
        print(div, file=f)
        
        
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html


html = file_html(layout, CDN, "my plot")
with open('html_etgspec.html', 'w') as f:
        print(html, file=f)