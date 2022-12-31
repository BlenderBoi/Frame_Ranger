import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import AB_Functions
from Frame_Ranger.Utility_Function import OAM_Functions



class FR_OT_AB_Remove_Action(bpy.types.Operator):

    bl_idname = "fr_ab.remove_action"
    bl_label = "Remove Action"
    bl_description = "Remove an Action"
    bl_options = {"REGISTER", "UNDO"}

    index: bpy.props.IntProperty()
    cleanup: bpy.props.BoolProperty()

    def draw(self, context):

        layout = self.layout

        if self.cleanup:
            box = layout.box()
            box.label(text="This Affect All Objects in this File", icon="INFO")
            box.label(text="This will Check All Objects")
            box.label(text="And Remove Any Action Slot with Missing Actions")

        layout.prop(self, "cleanup", text="Clean Up")


    def invoke(self, context, event):

        action = None

        if len(bpy.data.actions) > self.index:
            action = bpy.data.actions[self.index]

        if action:
            if action.users > 0:

                return context.window_manager.invoke_props_dialog(self)

            else:
                return self.execute(context)





        else:
            return {'FINISHED'}




    def execute(self, context):

        if len(bpy.data.actions) > self.index:

            action = bpy.data.actions[self.index]

            if action is not None:

                Utility_Function.remove_action_from_file(action, cleanup = self.cleanup)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_AB_Remove_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
