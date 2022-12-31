
import bpy


class FR_MT_KU_Keyframe_Utils_Menu(bpy.types.Menu):
    bl_label = "Keyframe Utils"
    bl_idname = "FR_MT_KU_keyframe_utils_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("fr_ku.randomize_keyframes", text="Randomize Keyframes")



classes = [FR_MT_KU_Keyframe_Utils_Menu]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
