import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions



class FR_OT_FRM_Sort_Frame_Range_Set(bpy.types.Operator):

    bl_idname = "fr_frm.sort_frame_range_set"
    bl_label = "Sort Frame Range Set"
    bl_description = "Sort a Frame Range Set"
    bl_options = {'UNDO', 'REGISTER'}

    reverse: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):




        FRM_Functions.sort_set(reverse=self.reverse)

        Utility_Function.update_UI()

        return {'FINISHED'}



classes = [FR_OT_FRM_Sort_Frame_Range_Set]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
