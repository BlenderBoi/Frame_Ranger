import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import AB_Functions

class FR_OT_AB_Remove_Zero_User_Actions(bpy.types.Operator):
    """Remove Zero User Actions"""
    bl_idname = "fr_ab.remove_zero_user_actions"
    bl_label = "Remove Zero User Actions"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        scn = context.scene
        actions = bpy.data.actions

        for loop in actions:

            for index, action in enumerate(actions):

                if action.users == 0:

                    Utility_Function.remove_action_from_file(action, cleanup = False)



        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_AB_Remove_Zero_User_Actions]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
