
import bpy

from . import Add
from . import Remove
from . import Reorder
from . import Set_Frame_Range

from . import Add_Set
from . import Remove_Set
from . import Reorder_Set

modules = [Add, Remove, Reorder, Add_Set, Remove_Set, Reorder_Set, Set_Frame_Range]


#Clear Frame Range
#Frame Range Set

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
