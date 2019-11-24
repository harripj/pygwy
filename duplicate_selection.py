import gwy
import gtk

plugin_menu = "/Multidata/Propagate Selection..."
plugin_desc = "Display the current image and selected coordinates."
plugin_type = "PROCESS"


def run():
    c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
    _id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)

    # key = "/0/select/line"
    selections = [key for key in c.keys_by_name() if "/{}/select".format(_id) in key]
    # print(selections)

    # create new combo box
    combo = gtk.combo_box_new_text()
    # add in valid selection options
    for selection in selections:
        combo.append_text(selection)
    # set default value as first in selections list, otherwise -1: None
    combo.set_active(0 if len(selections) else -1)

    # set up generic dialogue window
    dialogue = gtk.Dialog(
        title="Choose Selection",
        flags=gtk.DIALOG_MODAL,
        buttons=(
            gtk.STOCK_CANCEL,
            gtk.RESPONSE_REJECT,
            gtk.STOCK_OK,
            gtk.RESPONSE_ACCEPT,
        ),
    )

    # add combobox widget to dialogue
    dialogue.get_content_area().pack_start(combo)

    # main loop and wait for user response
    dialogue.show_all()
    response = dialogue.run()

    # heavy lifting done below here...
    # is user pressed OK
    if response == gtk.RESPONSE_ACCEPT:
        key = selections[combo.get_active()]
        # for each datafield in container
        for _id0 in gwy.gwy_app_data_browser_get_data_ids(c):
            # copy line
            line = c[key].duplicate()
            # add to new datafield with new key
            c.set_object(gwy.gwy_key_from_name(key.replace(str(_id), str(_id0))), line)

    # kill dialogue
    dialogue.destroy()
