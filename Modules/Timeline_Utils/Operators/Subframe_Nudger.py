import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import TU_Functions

class FR_OT_TU_Subframe_Nudger(bpy.types.Operator):

    bl_idname = "fr_ut.subframe_nudger"
    bl_label = "Subframe Nudger"
    bl_description = "Subframe Nudger"
    bl_options = {'UNDO', 'REGISTER'}
    
    nudge_marker: bpy.props.BoolProperty(default=True)
    nudge_keyframes: bpy.props.BoolProperty(default=True)

    def draw(self, context):

        layout = self.layout
        layout.label(text="This is a Destructive Operator", icon="ERROR")
        layout.label(text="Please Back up Before Proceed", icon="INFO")
        layout.prop(self, "nudge_marker", text="Markers")
        layout.prop(self, "nudge_keyframes", text="Keyframes")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene


        if self.nudge_keyframes:
            TU_Functions.Nudge_Keyframe()
        if self.nudge_marker:
            TU_Functions.Nudge_TimelineMarker()


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TU_Subframe_Nudger]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
