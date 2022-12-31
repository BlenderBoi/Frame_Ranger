import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions


class FR_OT_FRM_Clear_Frame_Range(bpy.types.Operator):

    bl_idname = "fr_frm.clear_frame_range"
    bl_label = "Clear Frame Range"
    bl_description = "Clear Frame Range"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):

        FRM_Functions.clear_fr()


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_FRM_Clear_Frame_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
