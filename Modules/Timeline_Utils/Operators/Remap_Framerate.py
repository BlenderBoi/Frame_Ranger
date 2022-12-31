import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import TU_Functions

class FR_OT_TU_Remap_Framerate(bpy.types.Operator):

    bl_idname = "fr_ut.remap_framerate"
    bl_label = "Remap Framerate"
    bl_description = "Remap Framerate Keyframe"
    bl_options = {'UNDO', 'REGISTER'}
    
    remap_marker: bpy.props.BoolProperty(default=True)
    remap_keyframes: bpy.props.BoolProperty(default=True)
    remap_frame_range: bpy.props.BoolProperty(default=True)
    subframe: bpy.props.BoolProperty(default=False)
    remap_frame_range_manager: bpy.props.BoolProperty(default=True)
    remap_all_set: bpy.props.BoolProperty(default=False)
    remap_manual_frame_range: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a Destructive Operator", icon="ERROR")
        layout.label(text="Please Back up Before Proceed", icon="INFO")
        layout.prop(self, "remap_marker", text="Markers")
        layout.prop(self, "remap_keyframes", text="Keyframes")
        layout.prop(self, "remap_manual_frame_range", text="Action Manual Frame Range")
        layout.prop(self, "remap_frame_range", text="Frame Range")
        layout.prop(self, "subframe", text="Subframe")
        row = layout.row()
        row.prop(self, "remap_frame_range_manager", text="Frame Range Manager")
        if self.remap_frame_range_manager:
            row.prop(self, "remap_all_set", text="All Frame Range Set")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene
        old = scn.render.fps
        new = scn.remap_fps
        subframe = not self.subframe

        if not context.scene.render.fps == new:

            if self.remap_frame_range_manager:
                TU_Functions.RemapFrameRangeManager(self.remap_all_set, context, old, new, subframe)

            if self.remap_keyframes:
                TU_Functions.RemapKeyframe(old, new, subframe)
            if self.remap_marker:
                TU_Functions.RemapTimelineMarker(old, new, subframe)
                TU_Functions.RemapPoseMarker(old, new, subframe)

            if self.remap_frame_range:
                TU_Functions.RemapFrameRange(context, old, new, subframe)

            if self.remap_manual_frame_range:
                TU_Functions.RemapManualFrameRange(old, new, subframe)


            scn.render.fps = new


        # else:
        #     self.report({"INFO"}, "")

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TU_Remap_Framerate]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
