import bpy
from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import Timeline_Marker_Function




class FR_OT_TMM_Remove_Marker_Camera(bpy.types.Operator):

    bl_idname = "fr_tmm.remove_marker_camera"
    bl_label = "Remove Marker Camera"
    bl_description = "Remove Marker Camera"
    bl_options = {'UNDO', 'REGISTER'}
    
    Index : bpy.props.IntProperty()

    def execute(self, context):

        scn = context.scene
        markers = scn.timeline_markers

        if len(markers) > self.Index:
            marker = markers[self.Index]
            marker.camera = None


        Utility_Function.update_UI()

        return {'FINISHED'}













classes = [FR_OT_TMM_Remove_Marker_Camera]






def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
