import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from mpl_toolkits.basemap import Basemap

import geotiler

path = "EventsChData/completeWithCoordinates.csv"
df = pd.read_csv(path)

df = df[df.coordinates!='(None, None)']
df.reset_index(drop=True, inplace=True)

years = list()
for (i,r) in df.iterrows():
	y = r.date.split('-')[0]
	if (not y in years):
		years.append(str(y))
		
years.sort()

axis_color = 'lightgoldenrodyellow'
fig = plt.figure()
size_0 = 10
freq_0 = 3
# Draw the plot
ax = fig.add_subplot(111)

bbox = [5.75, 45.5, 10.75, 48.]

mm = geotiler.Map(extent=bbox, zoom=7)

img = geotiler.render_map(mm)

my_map = Basemap(llcrnrlon=bbox[0],llcrnrlat=bbox[1],urcrnrlon=bbox[2],urcrnrlat=bbox[3],
             resolution='i', area_thresh = 0.1, projection='merc', ax=ax)#,lat_0 = 46.75, lon_0 = 7.5)
my_map.imshow(img, interpolation='lanczos', origin='upper')
#my_map.drawcountries()
#Fill the globe with a blue color 
#my_map.drawmapboundary()
#Fill the continents with the land color
#my_map.fillcontinents(color='coral',lake_color='aqua')
#my_map.drawcoastlines()

def getLongLat(df):
	lats = [0.0] * len(df.index)
	lngs = [0.0] * len(df.index)
	for (i,r) in df.iterrows():
		tmp = r.coordinates[1:-1].split(',')
		lats[i] = float(tmp[0].strip(' '))
		lngs[i] = float(tmp[1].strip(' '))
	return (lngs,lats)

def getDFforYear(df, year):
	newDF = pd.DataFrame(columns=df.columns)
	for (i,r) in df.iterrows():
		if (year in r.date):
			newDF = newDF.append(r)
	newDF.reset_index(drop=True, inplace=True)
	return newDF

yearsToLongLat = dict()
print("all")
(lngs, lats) = getLongLat(df)
yearsToLongLat["all"] = my_map(lngs, lats)
for y in years:
	print(y)
	(lngs, lats) = getLongLat(getDFforYear(df, y))
	yearsToLongLat[y] = my_map(lngs, lats)
	
years.insert(0,"all")

(x, y) = yearsToLongLat["all"]
color = "#FF0000"
plot, = my_map.plot(x, y, 'ro', markersize=size_0, alpha=0.5)


# Add two sliders for tweaking the parameters
size_slider_ax  = fig.add_axes([0.25, 0.15, 0.65, 0.03], axisbg=axis_color)
size_slider = Slider(size_slider_ax, 'Size', 2, 100, valinit=size_0)

begin_slider_ax  = fig.add_axes([0.25, 0.1, 0.65, 0.03], axisbg=axis_color)
begin_slider = Slider(begin_slider_ax, 'begin year', int(years[1]), int(years[-1]), valinit=int(years[1]))

end_slider_ax  = fig.add_axes([0.25, 0.05, 0.65, 0.03], axisbg=axis_color)
end_slider = Slider(end_slider_ax, 'end year', int(years[1]), int(years[-1]), valinit=int(years[-1]))


def size_slider_on_changed(val):
	plot.set_ms(size_slider.val)
	fig.canvas.draw_idle()
size_slider.on_changed(size_slider_on_changed)

begin_year = int(years[1])
def begin_slider_on_changed(val):
	global begin_year
	print(begin_year, val, int(round(val)))
	if(int(round(val)) != begin_year):
		begin_year = int(round(val))
		plot.set_xdata([])
		plot.set_ydata([])
		for i in range (begin_year, end_year):
			(x,y) = yearsToLongLat[str(i)]
			plot.set_xdata(plot.get_xdata() + x)
			plot.set_ydata(plot.get_ydata() + y)
		fig.canvas.draw_idle()
	
begin_slider.on_changed(begin_slider_on_changed)

end_year = int(years[-1])
def end_slider_on_changed(val):
	global end_year
	print(end_year, val, int(round(val)))
	if(int(round(val)) != end_year):
		end_year = int(round(val))
		plot.set_xdata([])
		plot.set_ydata([])
		for i in range (begin_year, end_year):
			(x,y) = yearsToLongLat[str(i)]
			plot.set_xdata(plot.get_xdata() + x)
			plot.set_ydata(plot.get_ydata() + y)
		fig.canvas.draw_idle()
		
end_slider.on_changed(end_slider_on_changed)

	
# Add a button for resetting the parameters
reset_button_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')

def reset_button_on_clicked(mouse_event):
	size_slider.reset()
	plot.set_ms(size_slider.val)
reset_button.on_clicked(reset_button_on_clicked)

# Add a set of radio buttons for changing color
color_radios_ax = fig.add_axes([0.025, 0.5, 0.15, 0.15], axisbg=axis_color)
color_radios = RadioButtons(color_radios_ax, ('#FF0000', '#00FF00', '#0000FF'), active=0)

years_check_ax = fig.add_axes([0.8, 0.5, 0.2, 0.5], axisbg=axis_color)
years_check = CheckButtons(years_check_ax, years, actives=[True]+[False]*(len(years)-1))
check = ["all"]
def selectYearsOnClick(label):
	prev = check.copy()
	if(label in check):
		check.remove(label)
	else:
		check.append(label)
	if("all" in prev and "all" in check):
		return None
	elif(len(check) == 0):
		plot.set_xdata([])
		plot.set_ydata([])
	elif("all" in check):
		(x,y) = yearsToLongLat["all"]
		plot.set_xdata(x)
		plot.set_ydata(y)
	elif(len(check) > len(prev)):
		(x,y) = yearsToLongLat[label]
		plot.set_xdata(plot.get_xdata() + x)
		plot.set_ydata(plot.get_ydata() + y)
	else:
		for (i,y) in enumerate(check):
			if(i==0):
				(x,y) = yearsToLongLat[y]
				plot.set_xdata(x)
				plot.set_ydata(y)
			else:
				(x,y) = yearsToLongLat[y]
				plot.set_xdata(plot.get_xdata() + x)
				plot.set_ydata(plot.get_ydata() + y)
	fig.canvas.draw_idle()
			
years_check.on_clicked(selectYearsOnClick)

def color_radios_on_clicked(label):
	color = label
	plot.set_color(color)
	fig.canvas.draw_idle()


color_radios.on_clicked(color_radios_on_clicked)

plt.show()
