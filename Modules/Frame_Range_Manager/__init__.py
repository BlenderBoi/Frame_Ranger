
import bpy
from . import LIST_Frame_Range_Manager
from . import Panels

modules = [LIST_Frame_Range_Manager]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
