
import bpy
from . import Offset_Action
from . import Trim_Action
from . import Time_Scale_Action

from . import Offset_Selected
from . import Trim_Selected
from . import Time_Scale_Selected

modules = [Time_Scale_Selected, Trim_Selected, Offset_Selected, Offset_Action, Trim_Action, Time_Scale_Action]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
