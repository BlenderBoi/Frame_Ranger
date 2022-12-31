import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import AB_Functions



class FR_OT_AB_Toogle_Fake_Users(bpy.types.Operator):
    """Toogle Fake Users"""
    bl_idname = "fr_ab.toogle_fake_users"
    bl_label = "Toogle Fake Users"
    bl_options = {"REGISTER", "UNDO"}

    fake_user: bpy.props.BoolProperty()


    def execute(self, context):

        Actions = bpy.data.actions

        for Action in Actions:
            Action.use_fake_user = self.fake_user

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_AB_Toogle_Fake_Users]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
