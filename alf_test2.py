#import fsps
#import matplotlib
#import matplotlib.pyplot as plt
import numpy as np
#from astropy.io import ascii
import pandas

from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import figure, output_file, show, curdoc

# -------- #
f0 = pandas.read_csv('model/cont_z-1.0_age1.0.dat')
source = ColumnDataSource(data=dict(x=f0['wave'], y=f0['flux']))

f1 = pandas.read_csv('model/subcont4047_z-1.0_age1.0.dat')
f2 = pandas.read_csv('model/subcont4757_z-1.0_age1.0.dat')
f3 = pandas.read_csv('model/subcont5767_z-1.0_age1.0.dat')
f4 = pandas.read_csv('model/subcont8089_z-1.0_age1.0.dat')
f5 = pandas.read_csv('model/subcont9010_z-1.0_age1.0.dat')

source1 = ColumnDataSource(data=dict(x=f1['wave'], y=f1['flux']))
source2 = ColumnDataSource(data=dict(x=f2['wave'], y=f2['flux']))
source3 = ColumnDataSource(data=dict(x=f3['wave'], y=f3['flux']))
source4 = ColumnDataSource(data=dict(x=f4['wave'], y=f4['flux']))
source5 = ColumnDataSource(data=dict(x=f5['wave'], y=f5['flux']))

s0 = figure(x_range=(3500, 1e4), plot_width=600, plot_height=350, title=None)
s1 = figure(x_range=(4e3, 4.7e3), y_range=(0.6, 1.2), plot_width=200, plot_height=160, title=None)
s2 = figure(x_range=(4.7e3, 5.7e3), y_range=(0.6, 1.2), plot_width=200, plot_height=160, title=None)
s3 = figure(x_range=(5.7e3, 6.7e3), y_range=(0.6, 1.2), plot_width=200, plot_height=160, title=None)
s4 = figure(x_range=(8e3, 8.92e3), y_range=(0.75, 1.15), plot_width=300, plot_height=160, title=None)
s5 = figure(x_range=(9e3, 1.01e4), y_range=(0.85, 1.1), plot_width=300, plot_height=160, title=None)
for tem in [s0, s1, s2, s3, s4, s5]:
    tem.xaxis.axis_label = "Wavelength"
    tem.yaxis.axis_label = "Flux"

s0.line('x', 'y', source=source, line_width=1, line_alpha=0.75, line_color='black')
s1.line('x', 'y', source=source1, line_width=1, line_alpha=0.75, line_color='black')
s2.line('x', 'y', source=source2, line_width=1, line_alpha=0.75, line_color='black')
s3.line('x', 'y', source=source3, line_width=1, line_alpha=0.75, line_color='black')
s4.line('x', 'y', source=source4, line_width=1, line_alpha=0.75, line_color='black')
s5.line('x', 'y', source=source5, line_width=1, line_alpha=0.75, line_color='black')

Spectra = {}
ContSub1 = {}
ContSub2 = {}
ContSub3 = {}
ContSub4 = {}
ContSub5 = {}
    
for zmet in [-1, -0.8, -0.6, -0.4, -0.2, 0., 0.2]:
    for age in [1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13.]:
        
        fname = 'model/cont_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname1 = 'model/subcont4047_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname2 = 'model/subcont4757_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname3 = 'model/subcont5767_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname4 = 'model/subcont8089_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        fname5 = 'model/subcont9010_z'+str(round(zmet,1))+'_age'+str(round(age,1))+'.dat'
        Spectra[(int(zmet*10), (age))] = pandas.read_csv(fname)
        ContSub1[(int(zmet*10), (age))] = pandas.read_csv(fname1)
        ContSub2[(int(zmet*10), (age))] = pandas.read_csv(fname2)
        ContSub3[(int(zmet*10), (age))] = pandas.read_csv(fname3)
        ContSub4[(int(zmet*10), (age))] = pandas.read_csv(fname4)
        ContSub5[(int(zmet*10), (age))] = pandas.read_csv(fname5)
        
age = Slider(title="age", value=1., start=1., end=13., step=1.)
zmet = Slider(title="[Z/H]", value=-1., start=-1., end=0., step=0.2)

def update_data(attrname, old, new):
    tage = age.value
    zh = zmet.value
    
    fx = Spectra[(int(zh*10), int(tage))] 
    source.data = dict(x=fx['wave'], y=fx['flux'])
    
    fx1 = ContSub1[(int(zh*10), int(tage))] 
    source1.data = dict(x=fx1['wave'], y=fx1['flux'])
    
    fx2 = ContSub2[(int(zh*10), int(tage))] 
    source2.data = dict(x=fx2['wave'], y=fx2['flux'])
    
    fx3 = ContSub3[(int(zh*10), int(tage))] 
    source3.data = dict(x=fx3['wave'], y=fx3['flux'])
    
    fx4 = ContSub4[(int(zh*10), int(tage))] 
    source4.data = dict(x=fx4['wave'], y=fx4['flux'])
    
    fx5 = ContSub5[(int(zh*10), int(tage))] 
    source5.data = dict(x=fx5['wave'], y=fx5['flux'])


    
for w in [age, zmet]:
    w.on_change('value', update_data)

layout = column(
    widgetbox(age, zmet),
    s0, row(s1, s2, s3), row(s4, s5),
    
)
# initialize
curdoc().add_root(layout)


#from bokeh.plotting import figure, output_file, save
#output_file("alf_test2.html")
#save(layout)

#from bokeh.embed import components
#script, div = components(layout)
#print(script)
#print >> 'alf_test2_script.txt', script
#print >> 'alf_test2_div.txt', div