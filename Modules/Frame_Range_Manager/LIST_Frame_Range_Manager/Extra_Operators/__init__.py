
import bpy
# from . import FRM_Frame_Range_From_Marker
# from . import FRM_IO_Export_Frame_Range
# from . import FRM_IO_Import_Frame_Range
# from . import FRM_Batch_Rename
# from . import FRM_Set_Batch_Rename
# from . import FRM_Marker_From_Frame_Range
#

from . import Batch_Rename_Frame_Ranges
from . import Batch_Rename_Frame_Range_Sets

from . import Clear
from . import Sort

from . import Clear_Set
from . import Clear_Empty_Set
from . import Sort_Set

from . import IO_Export_Frame_Range
from . import IO_Import_Frame_Range

from . import Marker_From_Frame_Range
from . import Frame_Ranges_From_Marker


modules = [Marker_From_Frame_Range, Frame_Ranges_From_Marker, Batch_Rename_Frame_Ranges, Batch_Rename_Frame_Range_Sets, Clear, Sort, Clear_Set, Clear_Empty_Set, Sort_Set, IO_Import_Frame_Range, IO_Export_Frame_Range]

# modules = [FRM_Frame_Range_From_Marker, FRM_IO_Export_Frame_Range, FRM_IO_Import_Frame_Range, FRM_Batch_Rename, FRM_Set_Batch_Rename, FRM_Marker_From_Frame_Range]



def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
