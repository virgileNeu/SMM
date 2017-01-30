import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from mpl_toolkits.basemap import Basemap
import geotiler

#####FUNCTIONS##########################################################
def setMapZoom(my_map,zoom, img_dict = None):
	img = None
	if(img_dict != None and zoom in img_dict):
		img = img_dict[zoom]
	else:
		mm = geotiler.Map(extent=bbox, zoom=zoom)
		img = geotiler.render_map(mm)
		if(img_dict != None):
			img_dict[zoom] = img
	my_map.imshow(img, origin='upper')

def stringToLongLat(string):
	tmp = string[1:-1].split(',')
	return (tmp[0], tmp[1])

def getLongLat(df):
	lats = [0.0] * len(df.index)
	lngs = [0.0] * len(df.index)
	for (i,r) in df.iterrows():
		tmp = stringToLongLat(r.coordinates)
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

def size_slider_on_changed(val):
	plot.set_ms(size_slider.val)
	fig.canvas.draw_idle()

def zoomup_button_on_clicked(mouse_event):
	global current_zoom
	if(current_zoom < 20):
		current_zoom = current_zoom + 1
		global my_map
		global img_dict
		setMapZoom(my_map,current_zoom, img_dict)
		
def zoomdown_button_on_clicked(mouse_event):
	global current_zoom
	if(current_zoom > 3):
		current_zoom = current_zoom - 1
		global my_map
		global img_dict
		setMapZoom(my_map,current_zoom, img_dict)

def reset_button_on_clicked(mouse_event):
    size_slider.reset()
    global current_zoom
    global zoom_0
    current_zoom = zoom_0
    global my_map
    global img_dict
    setMapZoom(my_map,current_zoom, img_dict)
    plot.set_ms(size_slider.val)
    global af
    af.clearAnnote()

def color_radios_on_clicked(label):
	color = label
	plot.set_color(color)
	fig.canvas.draw_idle()

def anot_radios_on_clicked(label):
    global cid
    global fig
    global af
    fig.canvas.mpl_disconnect(cid)
    af.clearAnnote()
    af = anot.AnnoteFinder(x, y, df[label].tolist(), ax=ax)
    cid = fig.canvas.mpl_connect('button_press_event', af)
    fig.canvas.draw_idle()

def selectYearsOnClick(label):
	global check
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
########################################################################

debug = True

# Import Data
path = "/home/neu/Work/Applied_data_analysis/SMM/Scripts/events.ch/EventsChData/completeWithCoordinates.csv"
df = pd.read_csv(path)

# Clean Data
df = df[df.coordinates!='(None, None)']
df.reset_index(drop=True, inplace=True)

if(debug):
	df = df.head(100)

# years for checkboxes
years = list()
for (i,r) in df.iterrows():
	y = r.date.split('-')[0]
	if (not y in years):
		years.append(str(y))
years.sort()

# Prepare display window
fig = plt.figure(num=None, figsize=(18,9), dpi=96, facecolor='w', edgecolor='k')

size_0 = 10 # Default plot size
bbox = [5.75, 45.5, 10.75, 48.] # Switzerland (lngs, lats) box
zoom_0 = 8 # Default zoom
current_zoom = zoom_0 # Current Zoom
color = "#FF0000" # Current plot color
axiscolor = 'lightgoldenrodyellow'

# Set the map subplot
fig.subplots_adjust(left=0.05, right=0.95, bottom =0.05, top=0.95)
ax = fig.add_subplot(111)

# Set the map
my_map = Basemap(llcrnrlon=bbox[0],llcrnrlat=bbox[1],urcrnrlon=bbox[2],urcrnrlat=bbox[3],
             resolution='i', area_thresh = 0.1, projection='merc', ax=ax)

# Zoom -> map_image dictionary
img_dict = dict()

# Set OSM map image
setMapZoom(my_map, current_zoom, img_dict)

# Years -> (Lngs, Lats) dictionary
yearsToLongLat = dict()
if(debug):
	print("all")
(lngs, lats) = getLongLat(df)
yearsToLongLat["all"] = my_map(lngs, lats)
for y in years:
	if(debug):
		print(y)
	(lngs, lats) = getLongLat(getDFforYear(df, y))
	yearsToLongLat[y] = my_map(lngs, lats)
	
# add 'all' to checkboxes
years.insert(0,"all")

# Map (Lngs, Lats) -> event information dictionary
mapCoordToEvent = dict()
for i,r in df.iterrows():
	(lng,lat) = stringToLongLat(r.coordinates)
	(x, y) = my_map(float(lng), float(lat))
	key = (x,y)
	if key in mapCoordToEvent:
		mapCoordToEvent[key].append(r)
	else:
		mapCoordToEvent[key] = list(r)

# Initial plot with 'all' years
(x, y) = yearsToLongLat["all"]
plot, = my_map.plot(x, y, 'ro', markersize=size_0, alpha=0.5)


# Annotations on click
import anotg
af = anot.AnnoteFinder(x, y, df["artists"].tolist(), ax=ax)  #Artists
cid = fig.canvas.mpl_connect('button_press_event', af)

############# Interaction tools ########################################
# Size slider
size_slider_ax  = fig.add_axes([0.15, 0.01, 0.75, 0.03], axisbg=axiscolor)
size_slider = Slider(size_slider_ax, 'Size', 2, 100, valinit=size_0)
size_slider.on_changed(size_slider_on_changed)

# Zoom buttons
zoomup_button_ax = fig.add_axes([0.025,0.95,0.05,0.05])
zoomdown_button_ax = fig.add_axes([0.025,0.85,0.05,0.05])
zoomup_button = Button(zoomup_button_ax, '+', color = axiscolor)
zoomdown_button = Button(zoomdown_button_ax, '-', color = axiscolor)
zoomup_button.on_clicked(zoomup_button_on_clicked)
zoomdown_button.on_clicked(zoomdown_button_on_clicked)

# Reset button
reset_button_ax = fig.add_axes([0.025, 0.75, 0.05, 0.05],axisbg=axiscolor)
reset_button = Button(reset_button_ax, 'Reset', hovercolor='0.975', color = axiscolor)
reset_button.on_clicked(reset_button_on_clicked)

# Color radio buttons
color_radios_ax = fig.add_axes([0.025, 0.5, 0.1, 0.1],axisbg=axiscolor)
color_radios = RadioButtons(color_radios_ax, ('#FF0000', '#00FF00', '#0000FF'), active=0)
color_radios.on_clicked(color_radios_on_clicked)

# Annotation information radio buttons
anot_radios_ax = fig.add_axes([0.025, 0.2, 0.1, 0.1],axisbg=axiscolor)
anot_radios = RadioButtons(anot_radios_ax, ('artists', 'event'), active=0)
anot_radios.on_clicked(anot_radios_on_clicked)

# Years check box
years_check_ax = fig.add_axes([0.9, 0.35, 0.05, len(years)*0.05],axisbg=axiscolor)
years_check = CheckButtons(years_check_ax, years, actives=[True]+[False]*(len(years)-1))
check = ["all"]		
years_check.on_clicked(selectYearsOnClick)

########################################################################

# Display application
plt.show()
