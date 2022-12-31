
import bpy
from . import Property
from . import UI_List
from . import Extras_Menu 
from . import Operators
from . import Extra_Operators

modules = [Property, UI_List, Extras_Menu, Operators, Extra_Operators]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
