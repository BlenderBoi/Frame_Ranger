

import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

ENUM_Sort_By = [("NAME","Name","Name"),("SIZE","Range Size","Frame Range Size")]



class FR_OT_OAM_Sort_Action_Slot(bpy.types.Operator):

    bl_idname = "fr_oam.sort_action_slot"
    bl_label = "Sort Action"
    bl_description = "Sort Action Slot"
    bl_options = {'UNDO', 'REGISTER'}

    sort_by: bpy.props.EnumProperty(items=ENUM_Sort_By)
    reverse: bpy.props.BoolProperty(default=False)

    target_object: bpy.props.StringProperty()


    def draw(self, context):
        layout = self.layout
        layout.label(text="Sort By: ")
        layout.prop(self, "sort_by", text="")
        layout.prop(self, "reverse", text="Reverse")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:

            bpy.ops.fr_oam.clean_action_list(target_object=obj.name)
            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.sort(sort_by=self.sort_by, reverse=self.reverse)








        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Sort_Action_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
