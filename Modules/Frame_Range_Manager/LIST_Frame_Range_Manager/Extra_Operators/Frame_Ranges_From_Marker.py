import bpy
import itertools

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions
from Frame_Ranger.Utility_Function import Timeline_Marker_Function


mode = [("PAIR","Pair","Pair"),("SUFFIX","Suffix","Suffix"),("PREFIX","Prefix","Prefix")]

class FR_OT_FRM_Frame_Range_From_Marker(bpy.types.Operator):

    bl_idname = "fr_frm.frame_ranges_from_markers"
    bl_label = "Frame Range From Markers"
    bl_description = "Frame Range From Markers"
    bl_options = {'UNDO', 'REGISTER'}

    mode : bpy.props.EnumProperty(items=mode, default="PAIR")
    remove_overlapped : bpy.props.BoolProperty(default = True)

    #Future Feature
    pair_extension_start: bpy.props.StringProperty(default="_start")
    pair_extension_end: bpy.props.StringProperty(default="_end")

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "mode", text="Mode")
        layout.prop(self, "remove_overlapped", text="Remove Overlapped")


        if self.mode == "SUFFIX" or self.mode == "PREFIX":
            layout.prop(self, "pair_extension_start", text="Start")
            layout.prop(self, "pair_extension_end", text="End")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        if self.remove_overlapped:
            Timeline_Marker_Function.remove_overlapped_markers()



        FRM_Functions.frame_ranges_from_markers(self.mode, self.pair_extension_start, self.pair_extension_end)


        Utility_Function.update_UI()
        return {'FINISHED'}



classes = [FR_OT_FRM_Frame_Range_From_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
