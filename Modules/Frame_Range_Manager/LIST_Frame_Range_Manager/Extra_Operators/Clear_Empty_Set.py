import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions


class FR_OT_FRM_Clear_Empty_Frame_Range_Set(bpy.types.Operator):

    bl_idname = "fr_frm.clear_empty_frame_range_set"
    bl_label = "Clear Empty Frame Range Set"
    bl_description = "Clear Empty Frame Range Set"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):

        FRM_Functions.clear_empty_set()        



        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_FRM_Clear_Empty_Frame_Range_Set]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
