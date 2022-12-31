
from typing import Set
import bpy
from . import Add_Pose_Marker
from . import Remove_Pose_Marker
from . import Move_To_Pose_Marker
from . import Reorder_Pose_Marker
from . import Remove_Marker_Camera
from . import Set_Marker_Camera
# modules = [Reorder_Pose_Marker, Add_Pose_Marker, Remove_Pose_Marker, Move_To_Pose_Marker]

modules = [Set_Marker_Camera, Remove_Marker_Camera, Add_Pose_Marker, Remove_Pose_Marker, Reorder_Pose_Marker, Move_To_Pose_Marker]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
