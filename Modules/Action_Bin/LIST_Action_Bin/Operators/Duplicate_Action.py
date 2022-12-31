import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import AB_Functions




class FR_OT_AB_Duplicate_Action(bpy.types.Operator):

    bl_idname = "fr_ab.duplicate_action"
    bl_label = "Duplicate Action"
    bl_description = "Duplicate Action"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty()
    index: bpy.props.IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")



    def invoke(self, context, event):

        actions = bpy.data.actions
        if len(actions) > self.index:
            action = actions[self.index]
            self.name = action.name + "_Copy"

            return context.window_manager.invoke_props_dialog(self)
        else:
            return {'FINISHED'}

    def execute(self, context):


        action = AB_Functions.duplicate_action(self.index, self.name)
    

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_AB_Duplicate_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
