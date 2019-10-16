# CREATED BY PJH 2017
# works well on HAADF STEM images, not tested on SPM

import json
import os
import gwy
import math

# sort out all grain quantities to save
GRAIN_QUANTITIES = dict()

for key in dir(gwy):
    val = getattr(gwy, key)
    if type(val) is gwy.GrainQuantity:
        GRAIN_QUANTITIES[key] = val

# finished sorting grain quantities

# def median_level_batch(container, datafield_id=0, kernel_size=30):
#     '''
#     Do revolve arc background subtractions or batch load of images.

#     Parameters
#     ----------
#     containers: gwy.Container
#     datafield_id: int

#     '''
#     # get stored data key, usually index 0
#     data_key = os.path.join(os.sep, str(datafield_id), 'data')
#     # get datafield
#     datafield = container[data_key]
#     # copy datafield
#     datafield_median = datafield.duplicate()
#     datafield_median.filter_median(kernel_size)

#     # add background to container, under datafield id tree
#     container.set_object_by_name(os.path.join(data_key, 'background'), datafield_median)

#     # do bg subtraction
#     datafield.subtract(datafield, datafield_median)
#     datafield.data_changed()

#     # show in app (window not raised -> False)
#     gwy.gwy_app_data_browser_add_data_field(datafield_median, container, False)


# def gwy_get_datafields(fname):
#     '''
#     Goes through .gwy file and pulls out the datafields.
    
#     Parameters
#     ----------
#     file: str (path)
#         Path to .gwy file.
        
#     Returns
#     -------
#     datafields: list
#         List of DataFields in .gwy file as numpy arrays.
#     '''
#     c = gwy.gwy_file_load(fname)
    
#     datafields = []

#     for key in c.keys_by_name():
#         if not isinstance(c[key], gwy.DataField):
#             continue
        
#         size = len(c[key])**0.5
#         assert not size%1, 'DataField: {} is not square.'.format(key)
#         size = int(size)
        
#         datafields.append(c[key])
    
#     return datafields

def get_data_key(_id=0):
    '''
    Convenience function to get data key string.

    Parameters
    ----------
    _id: int
        Datafield identifier. Default is 0.

    Returns
    -------
    key: str
        Formatted data key.

    '''
    return os.path.join(os.sep, str(_id), 'data')

def get_gaussian_sigma():
    '''
    Convenience function that gets the gaussian sigma value from the filters toolbox setting.

    Size (FWHM) relates to sigma as FWHM = 2*sqrt(2*ln(2)) * sigma.

    Returns
    -------
    sigma: float
        Standard deviation of gaussian kernel.

    '''

    settings = gwy.gwy_app_settings_get()
    # get sigma from settings, ie. vlaue last used in toolbox->filters
    size = settings['/module/filter/gauss_size']
    # size (FWHM) relates to sigma as FWHM = 2*sqrt(2*ln(2)) * sigma
    return size / (2.*math.sqrt(2.*math.log(2.)))


def get_mask_key(_id=0):
    '''
    Convenience function to get mask key string.

    Parameters
    ----------
    _id: int
        Datafield identifier. Default is 0.

    Returns
    -------
    key: str
        Formatted mask key.

    '''
    return os.path.join(os.sep, str(_id), 'mask')

def set_mask_colour(container, _id, rgba=(0.75, 0., 0., 0.5)):
    '''

    Convenience function to set mask colour parameters within container.

    Parameters
    ----------
    container: gwy.Container
    _id: int
        Mask key in container.
    rgba: tuple of floats, length 4
        Values range from 0..1. (Red, Green, Blue, Alpha).
    
    '''
    mask_key = get_mask_key(_id)
    # set mask colour and opacity
    for color, val in zip(('red', 'green', 'blue', 'alpha'), rgba):
        container[os.path.join(mask_key, color)] = val

def get_relative_value(val, datafield):
    '''

    Gets the value val as a fraction of datafield's data range.

    Parameters
    ----------
    val: float
    datafield: gwy.Datafield

    Returns
    -------
    frac: float
        Val as a fraction of datafield's data range
    
    '''
    # get relative threshold
    _min = datafield.get_min()
    _max = datafield.get_max()
    _range = abs(float(_max - _min))

    return (val - _min) / _range

def create_mask(datafield, threshold, below=False):
    '''

    Convenience function to create a grain mask by threshold.

    Parameters
    ----------
    datafield: gwy.Datafield
        Datafield used for thresholding.
    threshold: float
        Threshold in datafield coordinates.
    below: bool, default is False
        If False marks grains above threshold, else below.

    Returns
    -------
    grains: gwy.Datafield
        Mask of grains
    '''

    # init grain field
    grains = datafield.new_alike(True)
    # calculate relative threshold
    relative_threshold = 100. * get_relative_value(threshold, datafield)
    # False marks values above threshold (foreground)
    datafield.grains_mark_height(grains, relative_threshold, below)

    return grains

# def median_level(datafield, container, kernel_size=60, show=False):
#     '''
#     Compute a median level of the data. Original data is changed, a copy of the original data is added to the container.
    
#     Parameters
#     ----------
#     datafield: gwy.DataField
#         Data to level.
#     container: gwy.Container
#         Container to add new levelled data to.
#     kernel_size: int
#         Median filter kernel size in pixels. Default is 20.
#     show: bool
#         Show the newly added data in the container after computation.
#         Defualt is False.
        
#     '''
#     # # add original data to container
#     # original_id = gwy.gwy_app_data_browser_add_data_field( \
#     #         datafield.duplicate(), container, False)
#     # # don't show background
#     # gwy.gwy_app_set_data_field_title(container, original_id, 'Original Data')
    
#     # compute levelled background
#     background = datafield.duplicate()
#     background.filter_median(kernel_size)

#     bg_id = gwy.gwy_app_data_browser_add_data_field(background, container, show)
#     gwy.gwy_app_set_data_field_title(container, bg_id, 'Background')
    
#     # subtract background from data
#     datafield.subtract_fields(datafield, background)
#     # show on screen
#     datafield.data_changed()

def save_all(containers, format='svg', palette='Gray'):
    '''
    Saves all open files to PNG image files in a folder in image directory.
    
    containers is a list of open containers...
    ...can be obtained by gwy.gwy_app_data_browser_get_containers()
    '''
    for c in containers:
        datafield_ids = gwy.gwy_app_data_browser_get_data_ids(c)
        # file name
        fname = gwy.gwy_file_get_filename_sys(c)
        fpath, image_name = os.path.split(fname)
        # fpath = fname.replace(image_name, '')
        
        image_name_no_format, extension = os.path.splitext(image_name)
        # dot_index = image_name.index('.')
        # image_name_no_format = image_name[:dot_index]
        # image_format = image_name[dot_index:]
                
        # SXM_channel_names_to_convert = ['Z (Forward)', 'Z (Backward)']
                
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
            image_name_string = image_name_no_format + '_{}.{}'.format(datafield_id, format)
            save_string = os.path.join(fpath, image_name_string)
            gwy.gwy_app_data_browser_select_data_field(c, datafield_id)
            gwy.gwy_file_save(c, save_string, gwy.RUN_NONINTERACTIVE)

# def save_gwy_grain_mask_to_JSON(container, datafield_id=0, grain_data_to_save=None):
#     '''
#     Calculate and save relevant parameters from a grain field on an image.
#     Takes mask field '/0/mask' from container and calculates grain parameters.
    
#     Saves container data (image, mask) and grain data to JSON file in
#     /Grain_Analysis folder in image directory.
#     Removes previous .json and previous .gwy file.
    
#     Default datafield_id=0 is usually main data in file.

#     Parameters
#     ----------
#     container: gwy.Container
#     datafield_id: int
#         Default 0. The gwy.DataField indentifying key. (0 is first dfield in container).
#     grain_data_to_save: dict or None
#         Default is None, in which case a new dictionary is created. Otherwise grain data is added to this dict.
#     '''
    
#     data_key = os.path.join(os.sep, str(datafield_id), 'data')
#     mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
    
#     # file name
#     fname = gwy.gwy_file_get_filename_sys(container)
#     fpath, image_name = os.path.split(fname)
#     image_name_no_format, _ext = os.path.splitext(image_name)
    
#     datafield = container.get_object_by_name(data_key)
#     grain_datafield = container.get_object_by_name(mask_key)
    
#     assert grain_datafield is not None, 'No mask found.'
    
#     numbered_grains = grain_datafield.number_grains()
    
#     # calculate grain parameters
#     # :::EDIT HERE TO SAVE DIFFERENT PARAMETERS:::
# #    values_to_compute = {'area' : gwy.GRAIN_VALUE_PROJECTED_AREA,
# #                         'pixel_area' : gwy.GRAIN_VALUE_PIXEL_AREA,
# #                         'eqv_disc_radius' : gwy.GRAIN_VALUE_EQUIV_DISC_RADIUS,
# #                         'eqv_ellipse_major' : gwy.GRAIN_VALUE_EQUIV_ELLIPSE_MAJOR,
# #                         'eqv_ellipse_minor' : gwy.GRAIN_VALUE_EQUIV_ELLIPSE_MINOR,
# #                         'mean' : gwy.GRAIN_VALUE_MEAN,
# #                         'curvature_x_center' : gwy.GRAIN_VALUE_CURVATURE_CENTER_X,
# #                         'curvature_y_center' : gwy.GRAIN_VALUE_CURVATURE_CENTER_Y,
# #                         'x_center': gwy.GRAIN_VALUE_CENTER_X,
# #                         'y_center': gwy.GRAIN_VALUE_CENTER_Y,
# #                         'boundary_length': gwy.GRAIN_VALUE_FLAT_BOUNDARY_LENGTH
# #                         }

#     # # dict with data computed
#     # if grain_data_to_save is None:
#     #     grain_data_to_save = dict()
#     # # save actual grain datafield mask as array. Will need to be unravelled
#     # grain_data_to_save['GRAIN_DATAFIELD'] = numbered_grains
#     # # save file name also
#     # grain_data_to_save['ORIGINAL_FILE_NAME'] = image_name

#     for key in GRAIN_QUANTITIES.keys():
#         grain_data_to_save[key] = datafield.grains_get_values( \
#                           numbered_grains, GRAIN_QUANTITIES[key])

# #    #save analysis in nested folder
# #    analysis_folder = os.path.join(fpath, 'Grain_Analysis')
# #    if not os.path.isdir(analysis_folder):
# #        os.mkdir(analysis_folder) # make folder if it doesn't exist
# #    
#     # save file to JSON
#     fname_json = os.path.join(fpath, image_name_no_format + '_grains.json')
#     # save container info as .gwy file in Grain_Analysis directory
#     fname_save = os.path.join(fpath, image_name_no_format + '.gwy')
    
#     # delete path if exists- allow a new file to be written
#     if os.path.exists(fname_json):
#         os.remove(fname_json)
#     # delete old gwy file if exists
#     if os.path.exists(fname_save):
#         os.remove(fname_save)
    
#     with open(fname_json, 'w') as save_file:
#         json.dump(grain_data_to_save, save_file)
        
#     gwy.gwy_file_save(container, fname_save, gwy.RUN_NONINTERACTIVE)

# def analyse_particles_otsu(container, datafield_id=0, filter_size=5,
#                            save=True):
#     '''
#     Marks grains on image as a mask. Grains are calculated using an Otsu
#     threshold. Removes grains touching image borders and noise (<5 px grains
#     (filter_size)).
    
#     Calls save_gwy_grains_mask_to_json function to save grain quantities.
    
#     '''
#     # create quark app key for mask. Not needed for datafield as it remains unchanged
#     # throughout this process
#     # key = gwy.gwy_app_get_data_key_for_id(datafield_id)
#     gwy.gwy_undo_checkpoint(container, container.keys_by_name()) # must be list of keys
    
#     data_key = os.path.join(os.sep, str(datafield_id), 'data')
#     mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
    
#     datafield = container.get_object_by_name(data_key)
    
#     # compute median level
#     #median_level(datafield, container)
    
#     # needed for batch processing
#     #if data is None:
#         # get current image data
#     #    datafields = gwyutils.get_data_fields_dir(container)
#         # for HAADF STEM data is stored in '/0/data' key
#     #    data = datafields[data_key]

#     # calculate otsu threshold after data offset normalisation, ie. data_min = 0
#     min_datarange = datafield.get_min()
#     max_datarange = datafield.get_max()
#     drange = abs(max_datarange - min_datarange)
    
#     # range is the same, ie max - min, offset shifted to 0
#     # datafield.renormalize(drange, 0)
#     # renormalised to help with relative threshold later
#     # otsu threshold
#     o_threshold = datafield.otsu_threshold()
#     # 100 for percentage
#     rel_threshold = 100 * (o_threshold-min_datarange)/drange

#     # new grain field
#     grain_datafield = datafield.new_alike(True)
    
#     # threshold --> false means mark above threshold
#     datafield.grains_mark_height(grain_datafield, rel_threshold, False)    
#     # remove grains touching image edegs -> skews data
#     grain_datafield.grains_remove_touching_border()
    
#     # median filter to despeckle, ie. remove grains of 5 pixel or less
#     # NB. AUGUST 2018
#     # median filter fucked with me for a year... below is what you want
#     grain_datafield.grains_remove_by_size(filter_size)
    
#     # add grain_datafield to gwyddion as mask field
#     container.set_object_by_name(mask_key, grain_datafield)
    
#     #mask_layer = gwy.LayerMask() # new gwy mask layer
#     #mask_layer.set_data_key(mask_key)
    
#     # set mask colour and opacity
#     container[os.path.join(mask_key, 'alpha')] = 0.25
#     container[os.path.join(mask_key, 'red')] = 1.0
    
#     if save:
#         save_gwy_grain_mask_to_JSON(container, datafield_id=datafield_id)
    
#     return grain_datafield
    
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

# def super_find_particles(container, datafield_id=0, save=True):
#     '''
#     Uses both Otsu method and blob finding by Laplacian of Gaussian to 
#     create a grain mask.
    
#     '''
#     # compute otsu threshold of OG data
#     otsu_datafield = analyse_particles_otsu(container,
#                                             datafield_id=datafield_id,
#                                             save=False)
#     # compute LoG
#     log_datafield, log_id = laplacian_of_gaussian(container,
#                                           datafield_id=datafield_id,
#                                           add_to_data_browser=False)
#     # compute otsu of LoG data
#     log_mask = analyse_particles_otsu(container,
#                                       datafield_id=log_id,
#                                       save=False)
    
    
#     # sums otsu and LoG otsu datafields
#     super_mask_datafield = otsu_datafield.new_alike(False)
#     # pointwise maxima
#     super_mask_datafield.max_of_fields(log_mask, otsu_datafield)
    
#     #print(super_mask_datafield.get_max(), super_mask_datafield.get_min())
    
#     mask_key = os.path.join(os.sep, str(datafield_id), 'mask')
#     container.set_object_by_name(mask_key, super_mask_datafield)
    
#     # set mask colour and opacity
#     container[os.path.join(mask_key, 'alpha')] = 0.4
#     container[os.path.join(mask_key, 'blue')] = 0.75
    
#     if save:
#         save_gwy_grain_mask_to_JSON(container, datafield_id)

def threshold_otsu_power(datafield, power=1./10):
    '''

    Calculates Otsu's threshold with power scaled data and sets a mask in container.

    Parameters
    ----------
    datafield: gwy.Datafield
    power: float, default is 1./10

    Returns
    -------
    mask: gwy.Datafield.
        Grain mask.

    '''

    # new array
    new = datafield.duplicate()
    # sets minimum data value to be zero to avoid power scaling errors
    new.add(-new.get_min())
    # raise data to power (typically less than one)
    new.set_data([math.pow(i, power) for i in new.get_data()])

    # # init grain field
    # grains = datafield.new_alike(True)
    # # calculate relative threshold
    # threshold = 100. * get_relative_value(new.otsu_threshold(), new)
    # # False marks values above threshold (foreground)
    # new.grains_mark_height(grains, threshold, False)

    return create_mask(new, new.otsu_threshold())

def threshold_otsu_median(datafield, pts=256):
    '''
    Compute Otsu's threshold with median classifier (histogram mode).

    Parameters
    ----------
    datafield: gwy.DataField
        Datafield over which threshold will be computed.
    pts: int
        Number of points in histogram. Default 256.

    Returns
    -------
    threshold: float

    '''
    # number of pts for histogram
    dl = gwy.DataLine(pts, 0, True)
    # compute z-scale histogram from image
    datafield.dh(dl, pts)

    # sort all intensity values
    vals = sorted(datafield.get_data())

    # sort out hist data
    dx = dl.get_real()/dl.get_res() # pixel spacing in data line
    offset = dl.get_offset() # dataline offset, ie. 0 index point value in x
    x = [(i*dx)+offset for i in range(pts)] # construct bin locations

    # calculate weights (CDF)
    cdf = gwy.DataLine(pts, 0, True)
    datafield.cdh(cdf, pts)
    weight1 = [int(round(i*len(vals))) for i in cdf.get_data()] # get cdf data as list
    weight2 = [max(weight1)-c for c in weight1[::-1]][::-1]

    # class medians for all possible thresholds
    median1 = [vals[:weight1[i]][weight1[i]//2] for i in range(0, pts-1)]
    median2 = [vals[weight1[i-1]:][(len(vals)-weight1[i-1])//2] for i in range(1, pts)]

    # median for whole image
    medianT = datafield.get_median()

    # Clip ends to align class 1 and class 2 variables:
    # The last value of `weight1`/`mean1` should pair with zero values in
    # `weight2`/`mean2`, which do not exist.
    variance = [weight1[i]*(median1[i]-medianT)**2 + weight2[i+1]*(median2[i]-medianT)**2 \
                for i in range(pts-1)]
    # get index of maximum variance to index x array
    threshold = x[:-1][variance.index(max(variance))]
    
    return threshold

def threshold_otsu_mode(datafield, pts=256):
    '''
    Compute Otsu's threshold with median classifier (histogram mode).

    Parameters
    ----------
    datafield: gwy.DataField
        Datafield over which threshold will be computed.
    pts: int
        Number of points in histogram. Default 256.

    Returns
    -------
    threshold: float

    '''
    # number of pts for histogram
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

    return threshold

def low_signal_threshold(container, _id=0):
    '''

    Creates a grain mask by blurring the image and then doing Otsu\'s power scaled threshold.
    The gaussian filtered image is added to the container.

    Parameters
    ----------
    container: gwy.container
    _id: int
        Key of data in container to process.

    '''
    # get sigma from settings, ie. value last used in toolbox->filters
    sigma = get_gaussian_sigma()
    # create undo point
    gwy.gwy_app_undo_checkpoint(container, container.keys_by_name())
    # get datafield 0 for each container for func to operate on
    data = container[get_data_key(_id)]
    # create new blurred data
    blurred = data.duplicate()
    # do gaussian filter
    blurred.filter_gaussian(sigma)
    # add to container
    gwy.gwy_app_data_browser_add_data_field(blurred, container, False)
    # create grain mask
    grains = threshold_otsu_power(blurred)
    # add grain field to container and set mask colour
    container.set_object_by_name(get_mask_key(_id), grains)
    set_mask_colour(container, _id)

def analyse_particles_otsu_median(container, datafield_id=0, filter_size=5,
                           save=False):
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
    
    # get datafield
    datafield = container.get_object_by_name(data_key)
    # calculate threhshold
    threshold = threshold_otsu_median(datafield)

    # --- CREATE MASK BELOW AND ADD TO CONTAINER

    grain_datafield = datafield.new_alike(True)
    # get relative threshold
    rel_threshold = 100. * get_relative_value(threshold, datafield)

    # threshold --> false means mark above threshold
    datafield.grains_mark_height(grain_datafield, rel_threshold, False)

    # NB. reordered operations remove_touching_border and area_filter
    # on date 5.2.2019
    # before this date order went border then size
    # grain_datafield.grains_remove_by_size(filter_size)

    # added 5.2.2019
    # grain_datafield_full = grain_datafield.duplicate()
    # container.set_object_by_name(os.path.join(os.sep, str(datafield_id), 'mask_including_edges'), \
    #                             grain_datafield_full)

    # remove grains touching image edegs -> skews data
    # grain_datafield.grains_remove_touching_border()

    container.set_object_by_name(mask_key, grain_datafield)
    
    # set mask colour and opacity
    container[os.path.join(mask_key, 'alpha')] = 0.25
    container[os.path.join(mask_key, 'blue')] = 1.0
    
    if save:
        save_dict = dict(THRESHOLD=threshold,
                         RELATIVE_THRESHOLD=rel_threshold,
                         GRAIN_DATAFIELD_INCLUDING_EDGES=grain_datafield_full.get_data())

        save_gwy_grain_mask_to_JSON(container, datafield_id=datafield_id, \
                                    grain_data_to_save=save_dict)
    
    return grain_datafield
