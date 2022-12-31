
import bpy
from . import Add_Action
from . import Remove_Action
from . import Duplicate_Action
from . import Select_Object_With_Action

modules = [Select_Object_With_Action,Duplicate_Action, Add_Action, Remove_Action]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
