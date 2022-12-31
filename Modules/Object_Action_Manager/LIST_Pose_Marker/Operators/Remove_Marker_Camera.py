import bpy
from Frame_Ranger import Utility_Function





class FR_OT_PMM_Remove_Marker_Camera(bpy.types.Operator):

    bl_idname = "fr_pmm.remove_marker_camera"
    bl_label = "Remove Pose Marker Camera"
    bl_description = "Remove Pose Marker Camera"
    bl_options = {'UNDO', 'REGISTER'}
    
    index : bpy.props.IntProperty()
    target_action: bpy.props.StringProperty()

    def execute(self, context):

        action = bpy.data.actions.get(self.target_action)

        if action is not None:

            markers = action.pose_markers

            if len(markers) > self.index:
                marker = markers[self.index]
                marker.camera = None


        Utility_Function.update_UI()

        return {'FINISHED'}













classes = [FR_OT_PMM_Remove_Marker_Camera]






def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
