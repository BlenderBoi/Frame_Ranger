
import bpy
from . import Constraint_Toogle 
from . import Bake_Deform_Armature


modules = [Bake_Deform_Armature, Constraint_Toogle]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
