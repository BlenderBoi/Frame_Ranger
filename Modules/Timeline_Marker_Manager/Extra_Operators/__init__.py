
from typing import Set
import bpy
from . import Clear_Timeline_Marker
from . import Clean_Timeline_Marker
from . import Batch_Rename_Timeline_Marker
from . import Remove_Timeline_Markers_By_Name
from . import Sort_Timeline_Marker
from . import IO_Import_Markers
from . import IO_Export_Markers
from . import Bind_Cameras_To_Markers_By_Name
from . import Remove_Non_Binded_Camera
from . import Remove_Marker_Camera
from . import Set_Marker_Camera


modules = [Set_Marker_Camera, Remove_Marker_Camera, Remove_Non_Binded_Camera, Bind_Cameras_To_Markers_By_Name, Clean_Timeline_Marker, IO_Import_Markers, IO_Export_Markers, Sort_Timeline_Marker, Clear_Timeline_Marker, Batch_Rename_Timeline_Marker, Remove_Timeline_Markers_By_Name]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
