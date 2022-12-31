import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

def Update_Range_Start(self, context):

    if self.start > self.end:
        self.end = self.start

def Update_Range_End(self, context):

    if self.end < self.start:
        self.start = self.end


class FR_OT_OAM_Add_Action_Slot(bpy.types.Operator):

    bl_idname = "fr_oam.add_action_slot"
    bl_label = "Add Action"
    bl_description = "Add Action"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty()

    start: bpy.props.IntProperty(update=Update_Range_Start, min = 0)
    end: bpy.props.IntProperty(update=Update_Range_End, min = 1)

    use_frame_range: bpy.props.BoolProperty(default=True)

    sync_range: bpy.props.BoolProperty(default=True)

    use_fake_user: bpy.props.BoolProperty(default=True)


    target_object: bpy.props.StringProperty()


    def draw(self, context):

        scn = context.scene
        layout = self.layout

        layout.prop(self, "name")

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

        row = layout.row(align=True)
        row.prop(self, "use_fake_user", text="Use Fake User")

    def invoke(self, context, event):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 
       
        if obj:
            
            if self.sync_range:
                scn.FR_TU_Autofit_Keyframe = False


            self.start = scn.frame_start
            self.end = scn.frame_end

            slot_list = obj.action_list

            name = obj.name
            size = str(len(slot_list))

            self.name = "{}_action{}".format(name, size)

            return context.window_manager.invoke_props_dialog(self)

        else:
            self.report({"INFO"}, "No Object Found")
            return self.execute(context)


    def execute(self, context):

        preferences = Utility_Function.get_addon_preferences()

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            
            if self.sync_range:
                self.start = scn.frame_start
                self.end = scn.frame_end

            name = self.name
            use_frame_range = self.use_frame_range

            start = self.start
            end = self.end

            slot =  action_list_helper.load_new_action(name, use_fake_user=self.use_fake_user, update_index=True)
            action = slot.action
            
            action.use_frame_range = self.use_frame_range

            if self.use_frame_range:

                action.frame_start = start
                action.frame_end = end

            action_list_helper.sync_active_slot(use_curve_range=False, sync_frame_range_set=False)
             

            Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Add_Action_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
