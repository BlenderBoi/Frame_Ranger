
import bpy
from . import Add_Timeline_Marker
from . import Remove_Timeline_Marker
from . import Move_To_Timeline_Marker
from . import Reorder_Timeline_Marker

modules = [Reorder_Timeline_Marker, Add_Timeline_Marker, Remove_Timeline_Marker, Move_To_Timeline_Marker]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
