from __future__ import print_function
import matplotlib, pandas, numpy as np
import matplotlib.pyplot as plt
from bokeh.layouts import column, row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, Slider, Range1d, LabelSet, Label, Arrow, OpenHead, NormalHead, VeeHead
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
        Spectra[str(10000*int(zmet*10)+int(age))]=np.vstack((pandas.read_csv(fname)['wave'], pandas.read_csv(fname)['flux'], 
                                                 pandas.read_csv(fname1)['flux'], pandas.read_csv(fname2)['flux'], 
                                                 pandas.read_csv(fname3)['flux'], pandas.read_csv(fname4)['flux'], 
                                                 pandas.read_csv(fname5)['flux']))
                                                 



def alf_interact(doc):
    f0 = Spectra[str(10000*int(-1*10)+int(1))]  
    source = ColumnDataSource(data=dict(x=f0[0], y0=f0[1], y1=f0[2], y2=f0[3], y3=f0[4], y4=f0[5], y5=f0[6]))

    s0 = figure(x_range=(3500, 1.1e4), plot_width=800, plot_height=200, title=None)
    s1 = figure(x_range=(4e3, 4.7e3), y_range=(0.6, 1.25), plot_width=260, plot_height=200, title=None)
    s2 = figure(x_range=(4.7e3, 5.7e3), y_range=(0.6, 1.2), plot_width=260, plot_height=200, title=None)
    s3 = figure(x_range=(5.7e3, 6.7e3), y_range=(0.6, 1.2), plot_width=260, plot_height=200, title=None)
    s4 = figure(x_range=(8e3, 8.92e3), y_range=(0.75, 1.1), plot_width=390, plot_height=200, title=None)
    s5 = figure(x_range=(9e3, 1.01e4), y_range=(0.9, 1.1), plot_width=390, plot_height=200, title=None)
    for i, tem in enumerate([s0, s1, s2, s3, s4, s5]):
        tem.xaxis.axis_label = "Wavelength"
        tem.yaxis.axis_label = "Flux"
    for i, tem in enumerate([s1, s2, s3, s4, s5]):
        tem.yaxis.axis_label = "Continuum Normed\nFlux"
    for i, tem in enumerate([s0, s1, s2, s3, s4, s5]):
        tem.line('x', 'y'+str(i), source=source, line_width=1, line_alpha=0.75, line_color='black')

    age = Slider(title="age", value=1., start=1., end=13., step=1.)
    zmet = Slider(title="[Z/H]", value=-1., start=-1.1, end=0.2, step=0.1)

    def callback(attrname, old, new):
        tage = age.value
        zh = zmet.value
        fx = Spectra[str(10000*int(zh*10)+int(tage))]
        source.data = dict(x=fx[0], y0=fx[1], y1=fx[2], y2=fx[3], y3=fx[4], y4=fx[5], y5=fx[6])
        
    for w in [age, zmet]:
        w.on_change('value', callback)

    layout = column(
        widgetbox(age, zmet),
        s0, row(s1, s2, s3), row(s4, s5))

    doc.add_root(layout)
    
    
    #myplot_html = file_html(layout, CDN)
    # this HTML code is very long (~30 K), the cell below doesn't show all the code in NBviewer
    #print(myplot_html)
    #HTML(myplot_html)

    #output_file("test.html")
    #save(doc)
    
    textlist = ['G4300', "Hgamma"]
    for i, xloc in enumerate([(4281.375+4316.375)/2, (4331.25+4352.25)/2,]):
        citation = Label(x=xloc, y=1.18+(-1)**i*0.02, x_units='data', y_units='data',
                 text=textlist[i], render_mode='css', text_font_size='7pt')
        s1.add_layout(citation)
        s1.line([xloc, xloc], [1.14, 1.18])
                
    textlist = ['Hbeta', 'Mgb', 'Fe5270', 'Fe5335']
    for i, xloc in enumerate([(4847.875+4876.625)/2, (5160.125+5192.625)/2, (5245.650+5285.65)/2, (5312.125+5352.125)/2]):
        citation = Label(x=xloc, y=1.14+(-1)**i*0.02, x_units='data', y_units='data',
                 text=textlist[i], render_mode='css', text_font_size='7pt')
        s2.add_layout(citation)
        s2.line([xloc, xloc], [1.10, 1.14])
                
    textlist = ['NaD', 'TiO', 'TiO2',]
    for i, xloc in enumerate([(5876.875+5909.375)/2.,(5936.625+5994.125)/2., (6189.625+6272.125)/2.,]):
        citation = Label(x=xloc, y=1.16-(-1)**i*0.015, x_units='data', y_units='data',
                 text=textlist[i], render_mode='css', text_font_size='7pt')
        s3.add_layout(citation)
        s3.line([xloc, xloc], [1.10, 1.14])
        
    textlist = ['CaT',]
    for i, xloc in enumerate([8498, 8542, 8662]):
        if i==1:
            citation = Label(x=xloc, y=1.08, x_units='data', y_units='data',
                     text=textlist[0], render_mode='css', text_font_size='7pt')
            s4.add_layout(citation)
        s4.line([xloc, xloc], [1.05, 1.08])
        
    textlist = ['NaI',]
    for i, xloc in enumerate([(8168.5+8234.125)/2.,]):
        citation = Label(x=xloc, y=1.08, x_units='data', y_units='data',
                 text=textlist[i], render_mode='css', text_font_size='7pt')
        s4.add_layout(citation)
        s4.line([xloc, xloc], [1.06, 1.08])
        
    textlist = ['FeH',]
    for i, xloc in enumerate([9920,]):
        citation = Label(x=xloc, y=1.08, x_units='data', y_units='data',
                 text=textlist[i], render_mode='css', text_font_size='7pt')
        s5.add_layout(citation)
        s5.line([xloc, xloc], [1.06, 1.08])
        
    from bokeh.io import export_svgs
    s0.output_backend = "svg"
    export_svgs(layout, filename="plot.svg")
    

server = Server({'/': alf_interact}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on https://menggu-astro.github.io/outreach/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()