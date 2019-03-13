# CREATED BY PJH 2017
# works well on HAADF STEM images, not tested on SPM

import json
import os
import gwy

# sort out all grain quantities to save
grain_quantities = dict()

for key in dir(gwy):
    val = getattr(gwy, key)
    if type(val) is gwy.GrainQuantity:
        grain_quantities[key] = val
# finished sorting grain quantities

def median_level_batch(container, datafield_id=0, kernel_size=30):
    '''
    Do revolve arc background subtractions or batch load of images.

    Parameters
    ----------
    containers: gwy.Container
    datafield_id: int

    '''
    # get stored data key, usually index 0
    data_key = os.path.join(os.sep, str(datafield_id), 'data')
    # get datafield
    datafield = container[data_key]
    # copy datafield
    datafield_median = datafield.duplicate()
    datafield_median.filter_median(kernel_size)

    # add background to container, under datafield id tree
    container.set_object_by_name(os.path.join(data_key, 'background'), datafield_median)

    # do bg subtraction
    datafield.subtract(datafield, datafield_median)
    datafield.data_changed()

    # show in app (window not raised -> False)
    gwy.gwy_app_data_browser_add_data_field(datafield_median, container, False)


def gwy_get_datafields(fname):
    '''
    Goes through .gwy file and pulls out the datafields.
    
    Parameters
    ----------
    file: str (path)
        Path to .gwy file.
        
    Returns
    -------
    datafields: list
        List of DataFields in .gwy file as numpy arrays.
    '''
    c = gwy.gwy_file_load(fname)
    
    datafields = []

    for key in c.keys_by_name():
        if not isinstance(c[key], gwy.DataField):
            continue
        
        size = len(c[key])**0.5
        assert not size%1, 'DataField: {} is not square.'.format(key)
        size = int(size)
        
        datafields.append(c[key])
    
    return datafields

def median_level(datafield, container, kernel_size=20, show=False):
    '''
    Compute a median level of the data. Original data is changed, a copy of the original data is added to the container.
    
    Parameters
    ----------
    datafield: gwy.DataField
        Data to level.
    container: gwy.Container
        Container to add new levelled data to.
    kernel_size: int
        Median filter kernel size in pixels. Default is 20.
    show: bool
        Show the newly added data in the container after computation.
        Defualt is False.
        
    '''
    # add original data to container
    original_id = gwy.gwy_app_data_browser_add_data_field( \
            datafield.duplicate(), container, False)
    # don't show background
    gwy.gwy_app_set_data_field_title(container, original_id, 'Original Data')
    
    # compute levelled background
    background = datafield.duplicate()
    background.filter_median(kernel_size)

    bg_id = gwy.gwy_app_data_browser_add_data_field(background, container, show)
    gwy.gwy_app_set_data_field_title(container, bg_id, 'Background')
    
    # subtract background from data
    datafield.subtract_fields(datafield, background)
    # show on screen
    datafield.data_changed()

def save_all_open_to_PNG(containers):
    '''
    Saves all open files to PNG image files in a folder in image directory.
    
    containers is a list of open containers...
    ...can be obtained by gwy.gwy_app_data_browser_get_containers()
    '''
    for c in containers:
        datafield_ids = gwy.gwy_app_data_browser_get_data_ids(c)
        #file name
        fname = gwy.gwy_file_get_filename_sys(c)
        fpath, image_name = os.path.split(fname)
        #fpath = fname.replace(image_name, '')
        
        image_name_no_format, extension = os.path.splitext(image_name)
        #dot_index = image_name.index('.')
        #image_name_no_format = image_name[:dot_index]
        #image_format = image_name[dot_index:]
                
        SXM_channel_names_to_convert = ['Z (Forward)', 'Z (Backward)']
                
        for datafield_id in datafield_ids:
            # retrieve datafield number in container from key
            #(for example '/0/data')
            # gets first non-empty element from key, eg. 0 from '/0/data'
            #datafield_id = int(filter(None, key.split('/')).pop(0))
            channel = gwy.gwy_app_get_data_field_title(c, datafield_id)
                    
            #FOR .SXM (or .sxm) IMAGES
            if extension.lower() == '.sxm':
                if channel not in SXM_channel_names_to_convert:
                    continue
                                    
            # set palette of datafield
            c.set_string_by_name('/%d/base/palette' % datafield_id, 'Gray')
                            
            #save images in nested folder
#            png_folder = os.path.join(fpath, 'PNG')
#            if not os.path.exists(png_folder):
#                os.makedirs(png_folder)
#            else:
#                # if file already exists, check it is a folder
#                assert os.path.isdir(png_folder), '{} exists and is not \
#                    a folder. Aborting save.'.format(png_folder)
                                                                                       
            #save
            image_name_string = image_name_no_format + '_' + channel + '.png'
            save_string = os.path.join(fpath, image_name_string)
            gwy.gwy_app_data_browser_select_data_field(c, datafield_id)
            gwy.gwy_file_save(c, save_string, gwy.RUN_NONINTERACTIVE)

def save_gwy_grain_mask_to_JSON(container, datafield_id=0, grain_data_to_save=None):
    '''
    Calculate and save relevant parameters from a grain field on an image.
    Takes mask field '/0/mask' from container and calculates grain parameters.
    
    Saves container data (image, mask) and grain data to JSON file in
    /Grain_Analysis folder in image directory.
    Removes previous .json and previous .gwy file.
    
    Default datafield_id=0 is usually main data in file.

    Parameters
    ----------
    container: gwy.Container
    datafield_id: int
        Default 0. The gwy.DataField indentifying key. (0 is first dfield in container).
    grain_data_to_save: dict or None
        Default is None, in which case a new dictionary is created. Otherwise grain data is added to this dict.
    '''
    
    data_key = os.path.join(os.sep, str(datafield_id), 'data')
    mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
    
    # file name
    fname = gwy.gwy_file_get_filename_sys(container)
    fpath, image_name = os.path.split(fname)
    image_name_no_format, _ext = os.path.splitext(image_name)
    
    datafield = container.get_object_by_name(data_key)
    grain_datafield = container.get_object_by_name(mask_key)
    
    assert grain_datafield is not None, 'No mask found.'
    
    numbered_grains = grain_datafield.number_grains()
    
    # calculate grain parameters
    # :::EDIT HERE TO SAVE DIFFERENT PARAMETERS:::
#    values_to_compute = {'area' : gwy.GRAIN_VALUE_PROJECTED_AREA,
#                         'pixel_area' : gwy.GRAIN_VALUE_PIXEL_AREA,
#                         'eqv_disc_radius' : gwy.GRAIN_VALUE_EQUIV_DISC_RADIUS,
#                         'eqv_ellipse_major' : gwy.GRAIN_VALUE_EQUIV_ELLIPSE_MAJOR,
#                         'eqv_ellipse_minor' : gwy.GRAIN_VALUE_EQUIV_ELLIPSE_MINOR,
#                         'mean' : gwy.GRAIN_VALUE_MEAN,
#                         'curvature_x_center' : gwy.GRAIN_VALUE_CURVATURE_CENTER_X,
#                         'curvature_y_center' : gwy.GRAIN_VALUE_CURVATURE_CENTER_Y,
#                         'x_center': gwy.GRAIN_VALUE_CENTER_X,
#                         'y_center': gwy.GRAIN_VALUE_CENTER_Y,
#                         'boundary_length': gwy.GRAIN_VALUE_FLAT_BOUNDARY_LENGTH
#                         }

    # dict with data computed
    if grain_data_to_save is None:
        grain_data_to_save = dict()
    # save actual grain datafield mask as array. Will need to be unravelled
    grain_data_to_save['GRAIN_DATAFIELD'] = numbered_grains
    # save file name also
    grain_data_to_save['ORIGINAL_FILE_NAME'] = image_name

    for key in grain_quantities.keys():
        grain_data_to_save[key] = datafield.grains_get_values( \
                          numbered_grains, grain_quantities[key])

#    #save analysis in nested folder
#    analysis_folder = os.path.join(fpath, 'Grain_Analysis')
#    if not os.path.isdir(analysis_folder):
#        os.mkdir(analysis_folder) # make folder if it doesn't exist
#    
    # save file to JSON
    fname_json = os.path.join(fpath, image_name_no_format + '_grains.json')
    # save container info as .gwy file in Grain_Analysis directory
    fname_save = os.path.join(fpath, image_name_no_format + '.gwy')
    
    # delete path if exists- allow a new file to be written
    if os.path.exists(fname_json):
        os.remove(fname_json)
    # delete old gwy file if exists
    if os.path.exists(fname_save):
        os.remove(fname_save)
    
    with open(fname_json, 'w') as save_file:
        json.dump(grain_data_to_save, save_file)
        
    gwy.gwy_file_save(container, fname_save, gwy.RUN_NONINTERACTIVE)

def analyse_particles_otsu(container, datafield_id=0, filter_size=5,
                           save=True):
    '''
    Marks grains on image as a mask. Grains are calculated using an Otsu
    threshold. Removes grains touching image borders and noise (<5 px grains
    (filter_size)).
    
    Calls save_gwy_grains_mask_to_json function to save grain quantities.
    
    '''
    # create quark app key for mask. Not needed for datafield as it remains unchanged
    # throughout this process
    # key = gwy.gwy_app_get_data_key_for_id(datafield_id)
    gwy.gwy_undo_checkpoint(container, container.keys_by_name()) # must be list of keys
    
    data_key = os.path.join(os.sep, str(datafield_id), 'data')
    mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
    
    datafield = container.get_object_by_name(data_key)
    
    # compute median level
    #median_level(datafield, container)
    
    # needed for batch processing
    #if data is None:
        # get current image data
    #    datafields = gwyutils.get_data_fields_dir(container)
        # for HAADF STEM data is stored in '/0/data' key
    #    data = datafields[data_key]

    # calculate otsu threshold after data offset normalisation, ie. data_min = 0
    min_datarange = datafield.get_min()
    max_datarange = datafield.get_max()
    drange = abs(max_datarange - min_datarange)
    
    # range is the same, ie max - min, offset shifted to 0
    # datafield.renormalize(drange, 0)
    # renormalised to help with relative threshold later
    # otsu threshold
    o_threshold = datafield.otsu_threshold()
    # 100 for percentage
    rel_threshold = 100 * (o_threshold-min_datarange)/drange

    # new grain field
    grain_datafield = datafield.new_alike(True)
    
    # threshold --> false means mark above threshold
    datafield.grains_mark_height(grain_datafield, rel_threshold, False)    
    # remove grains touching image edegs -> skews data
    grain_datafield.grains_remove_touching_border()
    
    # median filter to despeckle, ie. remove grains of 5 pixel or less
    # NB. AUGUST 2018
    # median filter fucked with me for a year... below is what you want
    grain_datafield.grains_remove_by_size(filter_size)
    
    # add grain_datafield to gwyddion as mask field
    container.set_object_by_name(mask_key, grain_datafield)
    
    #mask_layer = gwy.LayerMask() # new gwy mask layer
    #mask_layer.set_data_key(mask_key)
    
    # set mask colour and opacity
    container[os.path.join(mask_key, 'alpha')] = 0.25
    container[os.path.join(mask_key, 'red')] = 1.0
    
    if save:
        save_gwy_grain_mask_to_JSON(container, datafield_id=datafield_id)
    
    return grain_datafield
    
def laplacian_of_gaussian(container, datafield_id=0, add_to_data_browser=True):
    '''
    Apply a Laplacian of Gaussian filter- useful for finding blobs on 
    images.
    
    '''
    # get copy of data to filter
    data_key = os.path.join(os.sep, str(datafield_id), 'data')
    # mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
    datafield = container.get_object_by_name(data_key)
    
    log_datafield = datafield.duplicate()
    # apply gaussian filter
    log_datafield.filter_gaussian(3)
    # define laplacian kernel
    kernel_size = 5
    kernel_laplacian = gwy.DataField(kernel_size, kernel_size, \
                                     datafield.get_xreal(), \
                                     datafield.get_yreal(), False)
    # 5x5 2d laplacian kernel
    kernel_laplacian.set_data([0,0,-1,0,0,\
                               0,-1,-2,-1,0,\
                               -1,-2,16,-2,-1,\
                               0,-1,-2,-1,0,\
                               0,0,-1,0,0])
    # apply laplacian filter
    log_datafield.convolve(kernel_laplacian)
    # get original data channel name
    datafield_title = gwy.gwy_app_get_data_field_title(container, datafield_id)
    # add datafield to container and make container active and return its id
    datafield_log_id = gwy.gwy_app_data_browser_add_data_field(log_datafield,
                                                               container,
                                                               add_to_data_browser)
    # set LoG data title
    gwy.gwy_app_set_data_field_title(container, datafield_log_id, \
                                     'LoG_' + datafield_title)
    
    return log_datafield, datafield_log_id 

def super_find_particles(container, datafield_id=0, save=True):
    '''
    Uses both Otsu method and blob finding by Laplacian of Gaussian to 
    create a grain mask.
    
    '''
    # compute otsu threshold of OG data
    otsu_datafield = analyse_particles_otsu(container,
                                            datafield_id=datafield_id,
                                            save=False)
    # compute LoG
    log_datafield, log_id = laplacian_of_gaussian(container,
                                          datafield_id=datafield_id,
                                          add_to_data_browser=False)
    # compute otsu of LoG data
    log_mask = analyse_particles_otsu(container,
                                      datafield_id=log_id,
                                      save=False)
    
    
    # sums otsu and LoG otsu datafields
    super_mask_datafield = otsu_datafield.new_alike(False)
    # pointwise maxima
    super_mask_datafield.max_of_fields(log_mask, otsu_datafield)
    
    #print(super_mask_datafield.get_max(), super_mask_datafield.get_min())
    
    mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
    container.set_object_by_name(mask_key, super_mask_datafield)
    
    # set mask colour and opacity
    container[os.path.join(mask_key, 'alpha')] = 0.4
    container[os.path.join(mask_key, 'blue')] = 0.75
    
    if save:
        save_gwy_grain_mask_to_JSON(container, datafield_id)
        
def analyse_particles_otsu_median(container, datafield_id=0, filter_size=5,
                           save=True):
    '''
    Compute grains on an image through histogram clustering, with the median of 
    the class (rather than the mean) as the class descriptor.
    (Translates closely to the mode of class z-scale histogram).
    
    DOI: 10.1016/j.aasri.2012.11.074
    
    Calculates threshold, then puts a mask on the image. Grains are saved
    as JSON and .gwy files.
    
    Parameters
    ----------
    container: gwy.Container
        Container where data is stored/shown.
    datafield_id: int
        The id of the data to analyse within container. Deafault is 0, ie. first data channel.
    filter_size: int
        Remove found grains smaller than this, in pixels. Default is 5.
    save: boolean
        Whether to save the data as JSON and .gwy. Default is True.
    
    Returns
    -------
    grain_datafield: gwy.DataField
        Binary datafield where grains are foreground.
    '''
    # key for putting data in container
    data_key = os.path.join(os.sep, str(datafield_id), 'data')
    mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
    
    datafield = container.get_object_by_name(data_key)
    
    # number of pts for histogram
    pts = 256
    dl = gwy.DataLine(pts, 0, True)
    # compute z-scale histogram from image
    datafield.dh(dl, pts)

    # sort out hist data
    dx = dl.get_real()/dl.get_res() # pixel spacing in data line
    offset = dl.get_offset() # dataline offset, ie. 0 index point value in x
    x = [(i*dx)+offset for i in range(pts)] # construct bin locations
    y = dl.get_data() # get histogram values

    weights = dl.duplicate()
    weights.cumulate()	# calculate cdf
    weights.multiply(dx)	# make sure cdf sums to 1
    weights = weights.get_data() # get cdf data as list

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

    # NB. reordered operations remove_touching_border and area_filter
    # on date 5.2.2019
    # before this date order went border then size
    grain_datafield.grains_remove_by_size(filter_size)

    # added 5.2.2019
    grain_datafield_full = grain_datafield.duplicate()
    container.set_object_by_name('grain_datafield_full', grain_datafield_full)

    # remove grains touching image edegs -> skews data
    # grain_datafield.grains_remove_touching_border()

    container.set_object_by_name(mask_key, grain_datafield)
    
    # set mask colour and opacity
    container[os.path.join(mask_key, 'alpha')] = 0.25
    container[os.path.join(mask_key, 'blue')] = 1.0
    
    if save:
        save_gwy_grain_mask_to_JSON(container, datafield_id=datafield_id, \
                                    grain_data_to_save=dict(THRESHOLD=threshold,
                                                            RELATIVE_THRESHOLD=rel_threshold))
    
    return grain_datafield
