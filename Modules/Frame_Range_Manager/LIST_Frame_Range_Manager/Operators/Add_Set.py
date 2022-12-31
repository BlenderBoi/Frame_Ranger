import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions

class FR_OT_FRM_Add_Frame_Range_Set(bpy.types.Operator):

    bl_idname = "fr_frm.add_frame_range_set"
    bl_label = "Add Frame Range Set"
    bl_description = "Add a new Frame Range Set"
    bl_options = {'UNDO', 'REGISTER'}
    
    name: bpy.props.StringProperty(default="RangeSet0")


    def invoke(self, context, event):

        scn = context.scene


        self.name = "RangeSet{}".format(FRM_Functions.get_set_size())

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene


        FRM_Functions.add_set(self.name)



        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_FRM_Add_Frame_Range_Set]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
