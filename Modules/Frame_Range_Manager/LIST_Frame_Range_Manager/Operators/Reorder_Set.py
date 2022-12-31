import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions

mode = [("DOWN", "Down", "Down"),("UP", "Up", "Up")]

class FR_OT_FRM_Reorder_Frame_Range_Set(bpy.types.Operator):

    bl_idname = "fr_frm.reorder_frame_range_set"
    bl_label = "Reorder Frame Range Set"
    bl_description = "Reorder a Frame Range Set"
    bl_options = {'UNDO', 'REGISTER'}
    
    index : bpy.props.IntProperty()
    mode : bpy.props.EnumProperty(items=mode)

    def execute(self, context):
        
        if self.mode == "UP":
            FRM_Functions.set_move_up()

        if self.mode == "DOWN":
            FRM_Functions.set_move_down()

        Utility_Function.update_UI()
        return {'FINISHED'}



classes = [FR_OT_FRM_Reorder_Frame_Range_Set]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
