import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions

ENUM_Sort_Mode = [("NAME","Name","Name"),("SIZE","Range Size","Range Size")]

class FR_OT_FRM_Sort_Frame_Range(bpy.types.Operator):

    bl_idname = "fr_frm.sort_frame_range"
    bl_label = "Sort Frame Range"
    bl_description = "Sort a Frame Range"
    bl_options = {'UNDO', 'REGISTER'}
    
    reverse: bpy.props.BoolProperty(default=False)
    mode: bpy.props.EnumProperty(items=ENUM_Sort_Mode)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "reverse", text="Reverse")
        layout.prop(self, "mode", text="Mode")


    def invoke(self, context, event):


        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):




        FRM_Functions.sort_fr(mode=self.mode, reverse=self.reverse)
        Utility_Function.update_UI()

        return {'FINISHED'}



classes = [FR_OT_FRM_Sort_Frame_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
