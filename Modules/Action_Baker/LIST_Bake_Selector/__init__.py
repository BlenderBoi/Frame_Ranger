
import bpy
from . import UI_List
from . import Property
from . import Extras_Menu
from . import Operators

modules = [Operators, UI_List, Property, Extras_Menu]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
