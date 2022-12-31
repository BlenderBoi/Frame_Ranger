import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions



class FR_OT_OAM_On_Auto_Frame_Range(bpy.types.Operator):

    bl_idname = "fr_oam.on_auto_frame_range"
    bl_label = "On Auto Frame Range"
    bl_description = "On Auto Frame Range"
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context):

        scn = context.scene

        
        if scn.FR_TU_Autofit_Keyframe:
            scn.FR_TU_Autofit_Keyframe = False
        else:
            scn.FR_TU_Autofit_Keyframe = True

        scn.FR_TU_Auto_Frame_Range_Settings.Mode = "ACTION"
        scn.FR_TU_Auto_Frame_Range_Settings.Action_Mode = "ACTION"




        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_On_Auto_Frame_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
