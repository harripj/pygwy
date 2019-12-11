import gwy
import gtk
import random

plugin_menu = "/Synthetic/Deposition/Objects (x10)..."
plugin_desc = "Generates many sythetic datafields."
plugin_type = "PROCESS"


def run():
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    settings = gwy.gwy_app_settings_get()

    for n in range(10):
        seed = random.randint(0, 2 ** 32 - 1)  # 32 bit
        settings["/module/obj_synth/seed"] = seed

        gwy.gwy_process_func_run("obj_synth", container, gwy.RUN_IMMEDIATE)
