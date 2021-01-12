"""
This script displays a dashboard of the average response times to incidents in New York in 2020
The response time averages are divided into all of 2020 and individual zipcodes
Users can select zipcodes from a dropdown menu which will update the line for the selected zipcode
"""
from bokeh.plotting import figure, curdoc
from random import random
from bokeh.models import Legend, Select, ColumnDataSource
from bokeh.layouts import column
import pandas as pd

def update_plot_1(attr, old, new):
    new_zip1=z1.value
    new_data ={}
    new_data['Months']=pre_avgs['Months']
    new_data['y1']=pre_avgs[str(new_zip1)]
    source1.data=new_data

def update_plot_2(attr, old, new):
    new_zip2=z2.value
    new_data ={}
    new_data['Months']=pre_avgs['Months']
    new_data['y2']=pre_avgs[str(new_zip2)]
    source2.data=new_data

#Read in preprocessed zip averages and overall 2020 avgs
pre_avgs=pd.read_csv("preprocessed.csv")
all_2020=pd.read_csv("all_avgs.csv")

#Add 2020 avgs and months as columns to pre_avgs
pre_avgs['All_2020']=all_2020['2020'].tolist()
pre_avgs['Months']=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']

#Create source for each zip line
source1 = ColumnDataSource(data={'Months':pre_avgs['Months'], 'y1':pre_avgs['10000']})
source2 = ColumnDataSource(data={'Months':pre_avgs['Months'], 'y2':pre_avgs['10001']})

#Create zipcode drop downs from column names
menu = list(pre_avgs.columns)[:-2]
#Create zipcode dropdowns with Select
z1=Select(title='Zipcode 1',value='10000', options=menu)
z2=Select(title='Zipcode 2',value='10001', options=menu)

months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
month_vals=[0,1,2,3,4,5,6,7,8]
monthly_avgs=all_2020['2020'].to_list()

# create figure and customize
p1=figure(title='311 Average Responses Time in NYC',x_range=months, plot_height=600, plot_width=600)
p1.xaxis.axis_label = 'Month'
p1.yaxis.axis_label = 'Avg Response Time (hours)'

# graph lines for each of the averages
g1=p1.line(x=months,y=monthly_avgs, line_width=2, line_color="red")
g2=p1.line(x='Months', y='y1', line_width=2, line_color='blue', source=source1)
g3=p1.line(x='Months', y='y2', line_width=2, line_color='green', source=source2)

# add a legend
legend=Legend(items=[("2020", [g1]),("Zipcode 1", [g2]), ("Zipcode 2", [g3])], orientation='horizontal')
p1.add_layout(legend,'below')

# update figure appropriately with changes to dropdown menu
z1.on_change('value', update_plot_1)
z2.on_change('value', update_plot_2)

curdoc().add_root(column(z1,z2,p1))
