import gwy
from functions.pygwy_functions import save_all

plugin_menu = "/Basic Operations/Export All/.tiff"
plugin_type = "PROCESS"
plugin_desc = """Exports all data in open containers to SVG in nested folder."""


def run():
    # get containers
    containers = gwy.gwy_app_data_browser_get_containers()

    save_all(containers, format="tiff")
