import bpy


def register():
    bpy.types.Action.pose_markers_index = bpy.props.IntProperty()


def unregister():
    del bpy.types.Action.pose_markers_index


if __name__ == "__main__":

    register()

