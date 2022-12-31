import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions



class FR_OT_OAM_Set_Active_Slot(bpy.types.Operator):

    bl_idname = "fr_oam.set_active_slot"
    bl_label = "Set Active Slot"
    bl_description = "Set Active Slot"
    bl_options = {"REGISTER", "UNDO"}

    index : bpy.props.IntProperty()
    target_object: bpy.props.StringProperty()

    def execute(self, context):

        scn = context.scene

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 


        if obj:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            slot = action_list_helper.get_slot(self.index)
            current_index = action_list_helper.get_active_index() 


            action_list_helper.set_active_index(self.index, sync=True)









        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Set_Active_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
