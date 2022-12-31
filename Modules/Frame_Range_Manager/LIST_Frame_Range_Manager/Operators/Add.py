import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions

def Update_Start(self, context):
    if self.start > self.end:
        self.end = self.start+1

def Update_End(self, context):
    if self.start > self.end:
        self.start = self.end-1


class FR_OT_FRM_Add_Frame_Range(bpy.types.Operator):

    bl_idname = "fr_frm.add_frame_range"
    bl_label = "Add Frame Range"
    bl_description = "Add a new Frame Range"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty()
    start: bpy.props.IntProperty(min=0, update=Update_Start)
    end: bpy.props.IntProperty(min=1, update=Update_End)

    sync_scene: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.prop(self, "name")
        row = layout.row(align=True)
        row.prop(self, "sync_scene", text="", icon="UV_SYNC_SELECT")

        if self.sync_scene:
            row.prop(scn, "frame_start")
            row.prop(scn, "frame_end")
        else:
            row.prop(self, "start")
            row.prop(self, "end")



    def invoke(self, context, event):

        scn = context.scene

        if self.sync_scene:
            scn.FR_TU_Autofit_Keyframe = False

        self.start = scn.frame_start
        self.end = scn.frame_end
        self.name = "Range{}".format(FRM_Functions.get_fr_size())

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene

        if self.sync_scene:

            self.start = scn.frame_start
            self.end = scn.frame_end


        FRM_Functions.add_fr(self.name, self.start, self.end)


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_FRM_Add_Frame_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
