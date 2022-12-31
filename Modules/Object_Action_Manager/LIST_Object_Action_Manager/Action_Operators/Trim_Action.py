import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


def Update_Range_Start(self, context):

    if self.start > self.end:
        self.end = self.start + 1

def Update_Range_End(self, context):

    if self.end < self.start:
        self.start = self.end - 1

Range_Mode = [(("KEYFRAME"),("Keyframe"),("Keyframe")),(("ACTION"),("Action"),("Action")),(("NONE"),("None"),("None"))]

class FR_OT_OAM_Trim_Action(bpy.types.Operator):
    bl_idname = "fr_oam.trim_action"
    bl_label = "Trim Action"
    bl_description = "Trim Local Action"
    bl_options = {"REGISTER", "UNDO"}



    index: bpy.props.IntProperty()
    target_object: bpy.props.StringProperty()

    insert_start_end: bpy.props.BoolProperty(default=True)
    offset_to_zero: bpy.props.BoolProperty(default=False)
    delete_outside_range: bpy.props.BoolProperty(default=True)

    sync_range: bpy.props.BoolProperty(default=True)
    start: bpy.props.IntProperty(min=0, update=Update_Range_Start)
    end: bpy.props.IntProperty(min=1, update= Update_Range_End)



    def invoke(self, context, event):

        obj = bpy.data.objects.get(self.target_object)
        scn = context.scene


        if obj is not None:
            scn.FR_TU_Autofit_Keyframe = False
            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.set_active_index(self.index, sync=True)
        
            return context.window_manager.invoke_props_dialog(self)
        

        return {'FINISHED'}


    def execute(self, context):



        obj = bpy.data.objects.get(self.target_object)
        scn = context.scene


        if obj is not None:

            if self.sync_range:
                self.start = scn.frame_start
                self.end = scn.frame_end

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action = action_list_helper.get_action(self.index)

            start = self.start
            end = self.end

            Utility_Function.OAM_Functions.Trim_Action(action, start, end, isInsertFrame=self.insert_start_end, isOffset=self.offset_to_zero, isDelete=self.delete_outside_range)
            action_list_helper.set_active_index(self.index, sync=True)

            # if action.use_frame_range:
            #     action.frame_start = self.start
            #     action.frame_end = self.end




        Utility_Function.update_UI()

        return {'FINISHED'}

    def draw(self, context):

        scn = context.scene

        layout = self.layout
        row = layout.row(align=True)

        row = layout.row(align=True)
        row.prop(self, "sync_range", text="", icon="UV_SYNC_SELECT")

        if self.sync_range:
            row.prop(scn, "frame_start", text="")
            row.prop(scn, "frame_end", text="")

        else:
            row.prop(self, "start", text="")
            row.prop(self, "end", text="")

        row = layout.row(align=True)

        row = layout.row(align=True)
        row.prop(self, "insert_start_end", text="Holding Keyframe")
        row = layout.row(align=True)
        row.prop(self, "offset_to_zero", text="Offset to Zero")
        row = layout.row(align=True)
        row.prop(self, "delete_outside_range", text="Delete Outside Range")


classes = [FR_OT_OAM_Trim_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
