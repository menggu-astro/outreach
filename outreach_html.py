import itertools, matplotlib, pandas, numpy as np
import matplotlib.pyplot as plt
from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Range1d, LabelSet, Label, Arrow, OpenHead, NormalHead, VeeHead
from bokeh.plotting import figure, output_file, show, curdoc, output_notebook, save
from bokeh.themes import Theme
import yaml
from bokeh.resources import CDN
from bokeh.embed import file_html

         
specdata = pandas.read_pickle("./specdata.pkl")
spec_cds = ColumnDataSource(specdata)

code = """
var tage = age.value;
var zh = zmet.value;
var flagx = Math.round(10000*tage)+Math.round(zh*10);
for (var i = 0; i < paramarr.length; i++){
  if (paramarr[i]==flagx){
      source.data['flux1'] = flux1set[i]
      source.data['flux2'] = flux2set[i]
      source.data['flux3'] = flux3set[i]
      source.data['flux4'] = flux4set[i]
      source.data['flux5'] = flux5set[i]
      source.data['flux6'] = flux6set[i]
  }
}
source.change.emit();
"""

#output_file("js_on_change.html")
flux1set = specdata['flux1']
flux2set = specdata['flux2']
flux3set = specdata['flux3']
flux4set = specdata['flux4']
flux5set = specdata['flux5']
flux6set = specdata['flux6']
paramarr = specdata['param'].values
wave = specdata['wave'][0]
flag = 10000*int(1.0)+int(-1.0*10)
for i in range(len(paramarr)):
    if paramarr[i]==flag:
        data0 = dict(wave = wave, flux1 = flux1set[i], flux2 = flux2set[i], 
                     flux3 = flux3set[i], flux4 = flux4set[i], 
                     flux5 = flux5set[i], flux6 = flux6set[i])
source = ColumnDataSource(data=data0)

s0 = figure(x_range=(3500, 1.1e4), plot_width=90, plot_height=30, title=None)
s1 = figure(x_range=(4e3, 4.7e3), y_range=(0.6, 1.25), plot_width=30, plot_height=20, title=None)
s2 = figure(x_range=(4.7e3, 5.7e3), y_range=(0.6, 1.2), plot_width=30, plot_height=20, title=None)
s3 = figure(x_range=(5.7e3, 6.7e3), y_range=(0.6, 1.2), plot_width=30, plot_height=20, title=None)
s4 = figure(x_range=(8e3, 8.92e3), y_range=(0.75, 1.1), plot_width=45, plot_height=20, title=None)
s5 = figure(x_range=(9e3, 1.01e4), y_range=(0.9, 1.1), plot_width=45, plot_height=20, title=None)
for i, tem in enumerate([s0, s1, s2, s3, s4, s5]):
    tem.xaxis.axis_label = "Wavelength"
    tem.yaxis.axis_label = "Flux"
for i, tem in enumerate([s1, s2, s3, s4, s5]):
    tem.yaxis.axis_label = "Continuum Normed\nFlux"
for i, tem in enumerate([s0, s1, s2, s3, s4, s5]):
    tem.line('wave', 'flux'+str(i+1), source=source, line_width=1, line_alpha=0.75, line_color='black')

callback = CustomJS(args=dict(source=source, flux1set=flux1set, flux2set=flux2set, 
                              flux3set=flux3set, flux4set=flux4set, 
                              flux5set=flux5set, flux6set=flux6set, paramarr=paramarr), code=code)
        
age_slider = Slider(title="age", value=1., start=1., end=13., step=1.)
zmet_slider = Slider(title="[Z/H]", value=-1., start=-1.1, end=0.2, step=0.1)
callback.args["age"] = age_slider
callback.args["zmet"] = zmet_slider
    
for w in [age_slider, zmet_slider]:
    w.js_on_change('value', callback)

layout = column(widgetbox(age_slider, zmet_slider), s0, row(s1, s2, s3), row(s4, s5))


def add_label(iplot, itext, ixloc, iyloc=1.1):
    citation = Label(x=ixloc, y=iyloc, x_units='data', y_units='data', 
                     text=itext, render_mode='css', text_font_size='7pt')
    iplot.add_layout(citation)
    iplot.line([ixloc, ixloc], [iyloc*0.95, iyloc*0.98])
    
textlist = ['G4300', "Hgamma"]
for i, xloc in enumerate([(4281.375+4316.375)/2, (4331.25+4352.25)/2,]):
    add_label(s1, textlist[i], xloc, 1.18+(-1)**i*0.02)
                
textlist = ['Hbeta', 'Mgb', 'Fe5270', 'Fe5335']
for i, xloc in enumerate([(4847.875+4876.625)/2, (5160.125+5192.625)/2, (5245.650+5285.65)/2, (5312.125+5352.125)/2]):
    add_label(s2, textlist[i], xloc, 1.14+(-1)**i*0.02)
    
textlist = ['NaD', 'TiO', 'TiO2', 'Halpha']
for i, xloc in enumerate([(5876.875+5909.375)/2.,(5936.625+5994.125)/2., (6189.625+6272.125)/2., 6562.8]):
    add_label(s3, textlist[i], xloc, 1.16-(-1)**i*0.015)
    

textlist = ['CaT',]
for i, xloc in enumerate([8498, 8542, 8662]):
    if i==1:
        citation = Label(x=xloc, y=1.08, x_units='data', y_units='data',
        text=textlist[0], render_mode='css', text_font_size='7pt')
        s4.add_layout(citation)
    s4.line([xloc, xloc], [1.05, 1.08]) 
 
 
textlist = ['NaI',]
for i, xloc in enumerate([(8168.5+8234.125)/2.,]):
    add_label(s4, textlist[i], xloc, 1.08)
        
textlist = ['FeH',]
for i, xloc in enumerate([9920,]):
    add_label(s5, textlist[i], xloc, 1.08)
    
output_file("outreach.html")
save(layout)