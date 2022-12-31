
import bpy
from . import Panels
from . import LIST_Action_Bin

modules = [LIST_Action_Bin]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
