import bpy


def MM_Marker_Chooser_Poll(self, item):
    return item.type == "CAMERA"

def register():
    bpy.types.Scene.timeline_markers_index = bpy.props.IntProperty()
    bpy.types.TimelineMarker.notes = bpy.props.StringProperty()


    bpy.types.Scene.MM_Marker_Chooser_Limit = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=MM_Marker_Chooser_Poll
    )
    bpy.types.Scene.MM_Marker_Chooser = bpy.props.PointerProperty(type=bpy.types.Object)





def unregister():
    del bpy.types.Scene.timeline_markers_index
    del bpy.types.TimelineMarker.notes


    del bpy.types.Scene.MM_Marker_Chooser_Limit
    del bpy.types.Scene.MM_Marker_Chooser



if __name__ == "__main__":
    register()

