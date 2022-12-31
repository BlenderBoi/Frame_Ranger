
import bpy
# from . import FR_TU_Modal_Operators
# from . import FR_TU_Remap_Framerate_Panel
# from . import FR_TU_Remap_Framerate
# from . import FR_TU_Subframe_Nudger
# from . import FR_TU_Animation_Player
# from . import FR_TU_Autofit_Framerange
from . import Operators
from . import Animation_Player
# from . import Remap_Framerate_Panel
from . import Autofit_Framerange
from . import FR_KU_Menu
from . import Panels

modules = [
    Animation_Player,
    Operators,
    Autofit_Framerange,
    Base_Panel,
]

# modules = [
#     FR_TU_Modal_Operators,
#     FR_TU_Remap_Framerate_Panel,
#     FR_TU_Remap_Framerate,
#     FR_TU_Subframe_Nudger,
#     FR_TU_Autofit_Framerange,
#     FR_TU_Animation_Player,
#
#     ]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
