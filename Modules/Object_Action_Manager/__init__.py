
import bpy
from . import LIST_Object_Action_Manager
from . import LIST_Pose_Marker
from . import Action_Bin_Adder_Panel

# Sync unsynced
from . import Panels

# modules = [LIST_Object_Action_Manager, LIST_Pose_Marker, Action_Bin_Adder_Panel]
modules = [LIST_Object_Action_Manager, Action_Bin_Adder_Panel, LIST_Pose_Marker]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
