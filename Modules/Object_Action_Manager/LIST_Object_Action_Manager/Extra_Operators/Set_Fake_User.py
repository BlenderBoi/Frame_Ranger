

import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


class FR_OT_OAM_Toogle_Fake_Users(bpy.types.Operator):

    bl_idname = "fr_oam.toogle_fake_users"
    bl_label = "Toogle Fake Users"
    bl_description = "Toogle Fake Users"
    bl_options = {'UNDO', 'REGISTER'}

    fake_user: bpy.props.BoolProperty()
    target_object: bpy.props.StringProperty()

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)

            actions = action_list_helper.collect_action_list()

            for action in actions:
                action.use_fake_user = self.fake_user










        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Toogle_Fake_Users]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
