import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function


class FR_OT_TMM_Clean_Markers(bpy.types.Operator):
    """Remove marker that have the same name and frame"""
    bl_idname = "fr_tmm.clean_markers"
    bl_label = "Clean Overlap Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    # remove_duplicated: bpy.props.BoolProperty(default=False)
    remove_overlapped: bpy.props.BoolProperty(default=True)

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

        if self.remove_overlapped:
            Timeline_Marker_Function.remove_overlapped_markers()
            scn = context.scene
            scn.timeline_markers_index = len(scn.timeline_markers)-1

        Utility_Function.update_UI()


        return {'FINISHED'}


classes = [FR_OT_TMM_Clean_Markers]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
