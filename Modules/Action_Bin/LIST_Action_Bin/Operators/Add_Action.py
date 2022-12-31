import bpy


from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import AB_Functions

def Update_Range_Start(self, context):

    if self.start > self.end:
        self.end = self.start

def Update_Range_End(self, context):

    if self.end < self.start:
        self.start = self.end

class FR_OT_AB_Add_Action(bpy.types.Operator):

    bl_idname = "fr_ab.add_action"
    bl_label = "Add Action"
    bl_description = "Add an Action"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty()

    start: bpy.props.IntProperty(update=Update_Range_Start, min = 0)
    end: bpy.props.IntProperty(update=Update_Range_End, min = 1)
    use_frame_range: bpy.props.BoolProperty(default=True)

    sync_range: bpy.props.BoolProperty(default=True)


    def draw(self, context):

        scn = context.scene

        layout = self.layout
        layout.prop(self, "name", text="Name")

        row = layout.row(align=True)
        if self.use_frame_range:

            row.prop(self, "sync_range", text="", icon="UV_SYNC_SELECT")

            if self.sync_range:
                row.prop(scn, "frame_start")
                row.prop(scn, "frame_end")

            else:
                row.prop(self, "start")
                row.prop(self, "end")

        row = layout.row(align=True)
        row.prop(self, "use_frame_range", text="Manual Frame Range")


    def invoke(self, context, event):

        actions = bpy.data.actions
        self.name = "Action{}".format(str(len(actions)))

        scn = context.scene
        self.start = scn.frame_start
        self.end = scn.frame_end





        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene
        name = self.name
        start = self.start
        end = self.end

        if self.sync_range:
            start = scn.frame_start
            end = scn.frame_end
            scn.FR_TU_Autofit_Keyframe = False

        else:
            start = self.start
            end = self.end


        action = AB_Functions.add_action(self.name)
        
        action.use_frame_range = self.use_frame_range

        if self.use_frame_range:
            action.frame_start = start
            action.frame_end = end 


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_AB_Add_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
