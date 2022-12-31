
import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


class FR_OT_OAM_Push_To_NLA(bpy.types.Operator):
    """Push to NLA"""
    bl_idname = "fr_oam.push_slot_action_to_nla"
    bl_label = "Push to NLA"
    bl_options = {'UNDO', 'REGISTER'}
   
    index: bpy.props.IntProperty()
    target_object: bpy.props.StringProperty()

    def execute(self, context):


        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 
       
        if obj:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.push_to_nla(self.index)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Push_To_NLA]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
