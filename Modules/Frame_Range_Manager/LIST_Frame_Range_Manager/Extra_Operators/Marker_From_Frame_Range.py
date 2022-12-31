import bpy
import itertools

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions




mode = [("PAIR","Pair","Pair"),("SUFFIX","Suffix","Suffix"),("PREFIX","Prefix","Prefix")]

class FR_OT_FRM_Markers_From_Frame_Range(bpy.types.Operator):

    bl_idname = "fr_frm.markers_from_frame_range"
    bl_label = "Markers from Frame Range"
    bl_description = "Markers from Frame Range"
    bl_options = {'UNDO', 'REGISTER'}

    mode : bpy.props.EnumProperty(items=mode, default="PAIR")
    pair_extension_start: bpy.props.StringProperty(default="_start")
    pair_extension_end: bpy.props.StringProperty(default="_end")

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "mode", text="Mode")

        if self.mode == "SUFFIX" or self.mode == "PREFIX":
            layout.prop(self, "pair_extension_start", text="Start")
            layout.prop(self, "pair_extension_end", text="End")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        FRM_Functions.markers_from_frame_range(self.mode, self.pair_extension_start, self.pair_extension_end)

        Utility_Function.update_UI()
        return {'FINISHED'}



classes = [FR_OT_FRM_Markers_From_Frame_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
