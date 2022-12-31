import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions



class FR_OT_OAM_Offset_Action(bpy.types.Operator):
    bl_idname = "fr_oam.offset_action"
    bl_label = "Offset Action"
    bl_description = "Offset Action"
    bl_options = {"REGISTER", "UNDO"}


    target_object: bpy.props.StringProperty()
    index: bpy.props.IntProperty()

    sync_range: bpy.props.BoolProperty(default=True)
    frame: bpy.props.IntProperty(min=0)


    def draw(self, context):
        
        layout = self.layout
        scn = context.scene 

        row = layout.row(align=True)
        row.prop(self, "sync_range", text="", icon="UV_SYNC_SELECT")

        if self.sync_range:
            row.prop(scn, "frame_current", text="")
        else:
            row.prop(self, "frame", text="")






    def invoke(self, context, event):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object)


        scn.FR_TU_Autofit_Keyframe = False


        if obj is not None:
            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            frame_range = action_list_helper.get_slot_frame_range_by_index(self.index, use_curve_range=False)

        
            self.frame = int(frame_range[0])
            scn.frame_current = int(frame_range[0]) 


        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):


        scn = context.scene
        obj = bpy.data.objects.get(self.target_object)


        if self.sync_range:
            self.frame = scn.frame_current


        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action = action_list_helper.get_action(self.index)

            frame_range = action_list_helper.get_slot_frame_range_by_index(self.index, use_curve_range=False)
            start = int(frame_range[0])
            end = int(frame_range[1])
            

            OAM_Functions.Offset_Action(action, self.frame, start, end)

            action_list_helper.set_active_index(self.index, sync=True)



            Utility_Function.update_UI()

        return {'FINISHED'}



classes = [FR_OT_OAM_Offset_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
