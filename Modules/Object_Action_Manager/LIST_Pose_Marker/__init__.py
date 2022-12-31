
import bpy
from . import UI_List
from . import Property
from . import Operators
from . import Extra_Operators
from . import Extras_Menu
from . import Range_Operators

modules = [Range_Operators, UI_List, Property, Extras_Menu, Operators, Extra_Operators]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
