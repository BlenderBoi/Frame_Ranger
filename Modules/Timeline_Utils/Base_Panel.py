import bpy
from Frame_Ranger import Utility_Function

class FR_PT_TU_Frame_Range_Remapper_Panel(bpy.types.Panel):

    bl_label = "Frame Range Remapper"



    def draw(self, context):
        layout = self.layout
        scn = context.scene
        row = layout.row()
        row.label(text="Framerate Remap:")
        row = layout.row()
        d_row = row.row()
        d_row.enabled = False
        # d_row = row.row()
        d_row.prop(scn.render, "fps", text="From")
        row.prop(scn, "remap_fps", text="To")
        row.operator("fr_ut.remap_framerate", text="Remap Framerate")
        row = layout.row()
        row.label(text="Subframe Nudger:")
        row = layout.row()
        row.operator("fr_ut.subframe_nudger", text="Nudge Subframe")

def register():

    bpy.types.Scene.remap_fps  = bpy.props.IntProperty(min=1, soft_max=120, default=24)
    # bpy.utils.register_class(FR_PT_TU_Frame_Range_Remapper_Panel)


def unregister():
    del bpy.types.Scene.remap_fps
    # bpy.utils.unregister_class(FR_PT_TU_Frame_Range_Remapper_Panel)


if __name__ == "__main__":
    register()
