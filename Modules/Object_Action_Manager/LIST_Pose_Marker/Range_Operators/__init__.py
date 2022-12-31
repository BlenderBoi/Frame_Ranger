
import bpy
from . import Add_Pose_Marker_As_Range 
from . import Match_Marker_Capitalization
from . import Find_And_Set_Marker_As_Range

modules = [Find_And_Set_Marker_As_Range, Add_Pose_Marker_As_Range, Match_Marker_Capitalization]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
