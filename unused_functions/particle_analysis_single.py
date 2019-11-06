#CREATED BY PJH 2017
#works well on HAADF STEM images, not tested on SPM

import gwy
from pygwy_functions import analyse_particles_otsu

plugin_menu = "/Grains/Analyse Particles/Otsu's Method/Single"
plugin_type = "PROCESS"
plugin_desc = '''Analyse particles on image. Works well for HAADF_STEM.
                This fn renormalises the image, thresholds by Otsu's method,
                and works out grain parameters.
                Saves data to JSON of same file name.'''

def run():
    # get current image data
    datafield_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    analyse_particles_otsu(container, datafield_id=datafield_id)
