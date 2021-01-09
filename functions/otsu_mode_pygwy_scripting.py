datafield_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

pts = 256
dl = gwy.DataLine(pts, 0, True)

import os
data_key = os.path.join(os.sep, str(datafield_id), 'data')
mask_key = os.path.join(os.sep, str(datafield_id), 'mask')

datafield = container.get_object_by_name(data_key)

datafield.dh(dl, pts)

gcm = gwy.GraphCurveModel()
gcm.set_data_from_dataline(dl, 0, pts-1)

gm = gwy.GraphModel()
# gcm_id = gm.add_curve(gcm)

# sort out hist data
dx = dl.get_real()/dl.get_res() # pixel spacing in data line
offset = dl.get_offset() # dataline offset, ie. 0 index point value in x
x = [(i*dx)+offset for i in range(pts)] # construct bin locations
y = dl.get_data() # get histogram values

weights = dl.duplicate()
weights.cumulate()	# calculate cdf

weights.multiply(dx)	# make sure cdf sums to 1

weights = weights.get_data()

# holder lists for modal values at different thresholds
mode1 = []
mode2 = []
modeT = x[y.index(dl.get_max())] # get modal value for distribution

# for each possible threshold value in histogram
for i in range(1, pts):
	mode1.append(x[y.index(dl.part_extract(0, i).get_max())])
	mode2.append(x[i + y[i:].index(dl.part_extract(i, pts-i).get_max())])

# calculate intraclass variance depending on the thresholds used
variance = []
for i in range(len(mode1)): # should be same as mode2, ie. pts-1
	variance.append(weights[:-1][i]*(mode1[i]-modeT)**2 + (1-weights[1:][i])*(mode2[i]-modeT)**2)

# get index of maximum variance to index x array
threshold = x[:-1][variance.index(max(variance))]


# --- CREATE MASK BELOW AND ADD TO CONTAINER

grain_datafield = datafield.new_alike(True)

min_datarange = datafield.get_min()
max_datarange = datafield.get_max()
drange = abs(max_datarange - min_datarange)

rel_threshold = 100 * (threshold-min_datarange)/drange

# threshold --> false means mark above threshold
datafield.grains_mark_height(grain_datafield, rel_threshold, False)    
# remove grains touching image edegs -> skews data
grain_datafield.grains_remove_touching_border()

grain_datafield.grains_remove_by_size(5)

container.set_object_by_name(mask_key, grain_datafield)
    
#mask_layer = gwy.LayerMask() # new gwy mask layer
#mask_layer.set_data_key(mask_key)
    
# set mask colour and opacity
container[os.path.join(mask_key, 'alpha')] = 0.25
container[os.path.join(mask_key, 'blue')] = 1.0
    


# GRAPH PLOTTING BELOW

#dl_v = gwy.DataLine(len(variance), dx, True)
#dl_v.set_data(variance)
#dl_v.set_offset(offset)

#gcm_v = gwy.GraphCurveModel()
#gcm_v.set_data_from_dataline(dl_v, 0, len(variance)-1)
#gm.add_curve(gcm_v)

#ff = gwy.GraphCurveModel()
#ff.set_data_from_dataline(weight1, 0, 0)
#gm.add_curve(ff)
#fff= gwy.GraphCurveModel()
#fff.set_data_from_dataline(weight2, 0, 0)
#gm.add_curve(fff)

#gwy.gwy_app_data_browser_add_graph_model(gm, container, True)
