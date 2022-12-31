
import bpy
from . import Panels
from . import LIST_Bake_Selector

modules = [LIST_Bake_Selector]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
