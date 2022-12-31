
import bpy
from . import Remap_Framerate 
from . import Subframe_Nudger
from . import Modal_Operators
from . import Randomize_Keyframes

modules = [
    Randomize_Keyframes,
    Modal_Operators,
    Remap_Framerate,
    Subframe_Nudger,
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
