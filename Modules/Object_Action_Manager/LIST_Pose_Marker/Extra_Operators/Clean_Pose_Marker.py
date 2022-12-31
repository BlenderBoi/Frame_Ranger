import bpy
from Frame_Ranger import Utility_Function


from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions


class FR_OT_PMM_Clean_Markers(bpy.types.Operator):
    """Remove marker that have the same name and frame"""
    bl_idname = "fr_pmm.clean_markers"
    bl_label = "Clean Overlap Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    # remove_duplicated: bpy.props.BoolProperty(default=False)
    remove_overlapped: bpy.props.BoolProperty(default=True)
    target_action: bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        # layout.prop(self, "remove_duplicated", text="Remove Duplicated")
        layout.prop(self, "remove_overlapped", text="Remove Overlapped")

    # def invoke(self, context, event):
    #     return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        #
        # if self.remove_duplicated:
        #     Utility_Function.MM_Functions.remove_duplicated_markers(context)

        action = bpy.data.actions.get(self.target_action) 

        if action is not None:
            if self.remove_overlapped:
                Pose_Marker_Functions.remove_overlapped_markers(action)
                action.pose_markers_index = len(action.pose_markers)-1

        Utility_Function.update_UI()


        return {'FINISHED'}


classes = [FR_OT_PMM_Clean_Markers]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
