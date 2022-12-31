import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions

class FR_OT_FRM_Remove_Frame_Range(bpy.types.Operator):

    bl_idname = "fr_frm.remove_frame_range"
    bl_label = "Remove Frame Range"
    bl_description = "Remove a Frame Range"
    bl_options = {'UNDO', 'REGISTER'}
    
    index : bpy.props.IntProperty()

    def invoke(self, context, event):

        FRM_Functions.remove_fr(self.index)

        Utility_Function.update_UI()
        return {'FINISHED'}



classes = [FR_OT_FRM_Remove_Frame_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
