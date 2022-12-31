import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


Rename_Mode = [("SUFFIX","Suffix","Suffix"),("PREFIX","Prefix","Prefix"),("REPLACE","Replace","Replace"),("REMOVE","Remove","Remove")]


class FR_OT_OAM_Duplicate_And_Replace_ALl_Slot(bpy.types.Operator):
    """Duplicate And Replace All Slot"""
    bl_idname = "fr_oam.duplicate_and_replace_all_slot"
    bl_label = "Duplicate And Replace All Slot"
    bl_options = {"REGISTER", "UNDO"}

    use_fake_user: bpy.props.BoolProperty(default=True)
    target_object: bpy.props.StringProperty()

    mode: bpy.props.EnumProperty(items=Rename_Mode)

    string_a: bpy.props.StringProperty(default="_copy")
    string_b: bpy.props.StringProperty()



    def draw(self, context):
        layout = self.layout

        layout.prop(self, "mode", text="Mode")
        if self.mode == "PREFIX":
            layout.prop(self, "string_a", text="Prefix")
        if self.mode == "SUFFIX":
            layout.prop(self, "string_a", text="Suffix")
        if self.mode == "REPLACE":
            layout.prop(self, "string_a", text="Find")
            layout.prop(self, "string_b", text="Replace")
        if self.mode == "REMOVE":
            layout.prop(self, "string_a", text="Remove")

        layout.prop(self, "use_fake_user", text="Use Fake User")

    def invoke(self, context, event):

        obj = bpy.data.objects.get(self.target_object) 

        if obj:
            
            return context.window_manager.invoke_props_dialog(self)

        return {'FINISHED'}

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 



        if obj:

            batch_rename_dict = {}
    
            batch_rename_dict["mode"] = self.mode
            batch_rename_dict["string_a"] = self.string_a
            batch_rename_dict["string_b"] = self.string_b


            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.duplicate_and_replace_all_slot(batch_rename_dict)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Duplicate_And_Replace_ALl_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
