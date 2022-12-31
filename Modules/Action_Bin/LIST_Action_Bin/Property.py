import bpy

from Frame_Ranger import Utility_Function



classes = []


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.AB_Index = bpy.props.IntProperty(min=0)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.AB_Index


if __name__ == "__main__":
    register()

