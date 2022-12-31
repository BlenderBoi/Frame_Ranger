import bpy
import random

from Frame_Ranger import Utility_Function

class FR_OT_KU_Randomize_Keyframes(bpy.types.Operator):

    bl_idname = "fr_ku.randomize_keyframes"
    bl_label = "Randomize Keyframes"
    bl_description = "Randomize Keyframes"
    bl_options = {'UNDO', 'REGISTER'}

    min_x: bpy.props.IntProperty(default=-5)
    max_x: bpy.props.IntProperty(default=5)

    min_y: bpy.props.FloatProperty(default=0)
    max_y: bpy.props.FloatProperty(default=0)

    seed: bpy.props.IntProperty(default=0)

    @classmethod
    def poll(cls, context):
        if context.space_data.type in ["DOPESHEET_EDITOR", "GRAPH_EDITOR"]:
            return True


    def draw(self, context):
        layout = self.layout
        row =layout.row(align=True)
        row.prop(self, "min_x", text="Min Range (Frame)")
        row.prop(self, "max_x", text="Max Range (Frame)")
        row =layout.row(align=True)
        row.prop(self, "min_y", text="Min Range (Value)")
        row.prop(self, "max_y", text="Max Range (Value)")

        layout.prop(self, "seed")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene
        bpy.ops.anim.channels_select_all(action="SELECT")
        kf = context.selected_editable_keyframes

        if kf:
            random.seed(self.seed)
            for key in kf:
                if self.max_x > self.min_x:
                    random_value = int(random.uniform(self.min_x, self.max_x))
                    key.co.x += random_value
                    key.handle_left.x += random_value
                    key.handle_right.x += random_value

                if self.max_y > self.min_y:
                    random_value = random.uniform(self.min_y, self.max_y)
                    key.co.y += random_value
                    key.handle_left.y += random_value
                    key.handle_right.y += random_value

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_KU_Randomize_Keyframes]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
