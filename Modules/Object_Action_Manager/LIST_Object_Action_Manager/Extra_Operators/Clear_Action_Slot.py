
import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


class FR_OT_OAM_Clear_Action_List(bpy.types.Operator):
    """Clear Action List"""
    bl_idname = "fr_oam.clear_action_list"
    bl_label = "Clear Action List"
    bl_options = {'UNDO', 'REGISTER'}
   
    remove_action: bpy.props.BoolProperty(default=False)
    target_object: bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "remove_action", text="Remove Action From File")

    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.clear(remove_action=self.remove_action)





        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Clear_Action_List]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
