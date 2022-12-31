import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions


Rename_Mode = [("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix"),("REPLACE","Replace","Replace")]

class FR_OT_FRM_Batch_Rename_Frame_Range_Sets(bpy.types.Operator):

    bl_idname = "fr_frm.batch_rename_frame_range_sets"
    bl_label = "Batch Rename Frame Range Sets"
    bl_description = "Batch Rename Frame Range Sets"
    bl_options = {'UNDO', 'REGISTER'}

    mode: bpy.props.EnumProperty(items=Rename_Mode)

    string_a: bpy.props.StringProperty()
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



    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):


        FRM_Functions.batch_rename_set(self.mode, self.string_a, self.string_b)


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_FRM_Batch_Rename_Frame_Range_Sets]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
