import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import AB_Functions



class FR_OT_AB_Clear_Action(bpy.types.Operator):
    """Clear Action"""
    bl_idname = "fr_ab.clear_action"
    bl_label = "Clear Action"
    bl_options = {"REGISTER", "UNDO"}

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

        return context.window_manager.invoke_props_dialog(self)



    def execute(self, context):

        while len(bpy.data.actions) > 0 :

            action = bpy.data.actions[0]
            Utility_Function.remove_action_from_file(action, cleanup = self.cleanup)


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_AB_Clear_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
