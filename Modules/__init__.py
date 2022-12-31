
import bpy
from . import Action_Bin 
from . import Object_Action_Manager
from . import Preferences
from . import Timeline_Marker_Manager
from . import Action_Baker
from . import Frame_Range_Manager
from . import Timeline_Utils


modules = [Timeline_Utils, Frame_Range_Manager, Preferences, Timeline_Marker_Manager, Action_Bin, Object_Action_Manager, Action_Baker]
def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
