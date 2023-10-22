bl_info = {
    "name": "Frame Ranger",
    "author": "BlenderBoi",
    "version": (3, 1, 1),
    "blender": (3, 1, 0),
    "description": "Utilities for Frame related operations",
    "warning": "",
    "doc_url": "https://frame-ranger.readthedocs.io/en/latest/index.html",
    "category": "Utility",
}

import bpy

from . import Modules
from . import Utility_Function
from . import Draw_Helper
import addon_utils

modules =  [Modules]

def register():

    
    for mod in addon_utils.modules():
        if mod.bl_info.get('name', (-1, -1, -1)) == "Frame Ranger Lite" and mod.bl_info.get('author', (-1, -1, -1)) == "BlenderBoi":
            if addon_utils.check(mod.__name__)[1]:
                addon_utils.disable(mod.__name__, default_set=True, handle_error=None)


    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
