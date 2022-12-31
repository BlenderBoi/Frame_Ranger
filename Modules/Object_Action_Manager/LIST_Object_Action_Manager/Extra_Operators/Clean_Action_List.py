

import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


class FR_OT_OAM_Clean_Action_List(bpy.types.Operator):
    """Clean Action List"""
    bl_idname = "fr_oam.clean_action_list"
    bl_label = "Clean Action list"
    bl_options = {'UNDO', 'REGISTER'}
    
    target_object: bpy.props.StringProperty()

    def execute(self, context):


        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.cleanup(sync=True)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Clean_Action_List]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
