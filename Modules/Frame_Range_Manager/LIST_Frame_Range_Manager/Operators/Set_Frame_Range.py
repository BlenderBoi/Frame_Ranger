import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions



class FR_OT_FRM_Set_Frame_Range(bpy.types.Operator):

    bl_idname = "fr_frm.set_frame_range"
    bl_label = "Set Frame Range"
    bl_description = "Set a Frame Range"
    bl_options = {'UNDO', 'REGISTER'}
    
    index : bpy.props.IntProperty()

    def execute(self, context):

        scn = context.scene


        scn.FR_TU_Autofit_Keyframe = False

        FRM_Functions.set_frame_range(self.index)
         



        Utility_Function.update_UI()

        return {'FINISHED'}



classes = [FR_OT_FRM_Set_Frame_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
