
import bpy
from . import Clear_Pose_Marker
from . import Batch_Rename_Pose_Marker
from . import Remove_Pose_Markers_By_Name
from . import Sort_Pose_Marker

from . import IO_Export_Markers
from . import IO_Import_Markers
from . import Clean_Pose_Marker

modules = [IO_Import_Markers, IO_Export_Markers, Clean_Pose_Marker, Sort_Pose_Marker, Clear_Pose_Marker, Batch_Rename_Pose_Marker, Remove_Pose_Markers_By_Name]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
