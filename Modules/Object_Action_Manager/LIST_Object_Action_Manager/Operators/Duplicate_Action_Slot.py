import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

class FR_OT_OAM_Duplicate_Action_Slot(bpy.types.Operator):
    """Duplicate Action Slot"""
    bl_idname = "fr_oam.duplicate_action_slot"
    bl_label = "Duplicate Action Slot"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty()
    index: bpy.props.IntProperty()
    replace_slot: bpy.props.BoolProperty(default=False)
    use_fake_user: bpy.props.BoolProperty(default=True)

    target_object: bpy.props.StringProperty()


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")
        layout.prop(self, "replace_slot", text="Replace Slot")
        layout.prop(self, "use_fake_user", text="Use Fake User")

    def invoke(self, context, event):

        obj = bpy.data.objects.get(self.target_object) 

        if obj:
            
            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action = action_list_helper.get_action(self.index)

            if action:
                self.name = action.name + "_Copy"
                return context.window_manager.invoke_props_dialog(self)

        return {'FINISHED'}

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj:
            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            new_slot = action_list_helper.duplicate_slot_by_index(self.index, self.name, replace_slot = self.replace_slot, use_fake_user=self.use_fake_user, update_index=True, below_slot=True)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Duplicate_Action_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
