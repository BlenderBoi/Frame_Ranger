
import bpy
from . import UI_List
from . import Operators
from . import Extra_Operators
from . import Extras_Menu
from . import Property

from . import Panels

modules = [Property, Operators, Extra_Operators, Extras_Menu, UI_List]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
