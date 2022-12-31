import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions



def Update_Range_Start(self, context):

    if self.start > self.end:
        self.end = self.start + 1

def Update_Range_End(self, context):

    if self.end < self.start:
        self.start = self.end - 1
#
# Range_Mode = [(("KEYFRAME"),("Keyframe"),("Keyframe")),(("ACTION"),("Action"),("Action")),(("NONE"),("Custom"),("Custom"))]

# Range_Mode = [(("KEYFRAME"),("Keyframe"),("Keyframe")),(("ACTION"),("Action"),("Action")), (("MARKERS"),("Marker"),("Marker")), (("NONE"),("None"),("None"))]
Scale_Mode = [(("REMAP"),("Remap"),("Remap")),(("RATE"),("Rate"),("Rate"))]
Scale_Origin = [(("CENTER"),("Center"),("Center")),(("START"),("Start"),("Start")),(("END"),("End"),("End")),(("FRAME"),("Frame"),("Frame"))]
Limit_Mode = [(("ALL"),("All"),("All")),(("RANGE"),("In Range"),("In Range"))]

class FR_OT_OAM_Time_Scale_Selected(bpy.types.Operator):
    bl_idname = "fr_oam.time_scale_selected"
    bl_label = "Time Scale Selected"
    bl_description = "Time Scale Selected"
    bl_options = {"REGISTER", "UNDO"}

    target_object: bpy.props.StringProperty()

    Limit_Mode: bpy.props.EnumProperty(items=Limit_Mode, default="ALL")

    sync_origin: bpy.props.BoolProperty(default=True)
    Scale_Rate: bpy.props.FloatProperty(default=1, min=0)
    Scale_Origin_Mode: bpy.props.EnumProperty(default="START", items=Scale_Origin)
    Scale_Origin: bpy.props.IntProperty()

    sync_range: bpy.props.BoolProperty(default=True)
    start: bpy.props.IntProperty(update=Update_Range_Start)
    end: bpy.props.IntProperty(update= Update_Range_End)

    src_start: bpy.props.IntProperty(min=0, update=Update_Range_Start)
    src_end: bpy.props.IntProperty(min=1, update= Update_Range_End)

    subframe: bpy.props.BoolProperty(default=False)
    reverse: bpy.props.BoolProperty(default=False)




    def invoke(self, context, event):

        obj = bpy.data.objects.get(self.target_object)
        scn = context.scene

        scn.FR_TU_Autofit_Keyframe = False
    



        return context.window_manager.invoke_props_dialog(self)




    def draw(self, context):

        scn = context.scene

        layout = self.layout.column(align=True)
        row = layout.row(align=True)

        scn = context.scene



        row.label(text="Timescale Rate")
        row.prop(self, "Scale_Rate", text="Rate")
        row = layout.row(align=True)

        row.label(text="Scale Origin Mode")
        row.prop(self, "Scale_Origin_Mode", text="")
        row = layout.row(align=True)

        if self.sync_origin:

            if self.Scale_Origin_Mode == "FRAME":
                row.prop(self, "sync_origin", text="", icon="UV_SYNC_SELECT")
                row.prop(scn, "frame_current", text="Scale Origin")

        else:

            if self.Scale_Origin_Mode == "FRAME":
                row.prop(self, "sync_origin", text="", icon="UV_SYNC_SELECT")
                row.prop(self, "Scale_Origin", text="Scale Origin")



        row = layout.row(align=True)

        row.prop(self, "subframe", text="Subframe")
        row.prop(self, "reverse", text="Reverse")
        # row.prop(self, "Limit_Mode", text="Limit Mode")
        # layout.separator()
        layout.separator()

    def execute(self, context):

        self.Limit_Mode = "ALL"


        scn = context.scene

        if self.sync_origin:
            self.Scale_Origin = scn.frame_current

        obj = bpy.data.objects.get(self.target_object)
        scn = context.scene

        if self.sync_range:
            self.start = scn.frame_start
            self.end = scn.frame_end
    
        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list = action_list_helper.get_action_list()

            for index, slot in enumerate(action_list): 

                if slot.select:
                    action = slot.action
                    frame_range = action_list_helper.get_slot_frame_range_by_index(index)

                    if self.reverse:
                        store_end = self.start
                        store_start = self.end
                    else:
                        store_start = self.start
                        store_end = self.end


                    limit = self.Limit_Mode
                    Source = [frame_range[0], frame_range[1]]

                    if self.Scale_Origin_Mode == "START":
                        Scale_Origin = frame_range[0]

                    if self.Scale_Origin_Mode == "END":
                        Scale_Origin = frame_range[1]

                    if self.Scale_Origin_Mode == "CENTER":
                        Scale_Origin = OAM_Functions.Mid_Point(frame_range[0], frame_range[1])

                    if self.Scale_Origin_Mode == "FRAME":
                        Scale_Origin = self.Scale_Origin

                    if self.Scale_Origin_Mode == "NONE":
                        Scale_Origin = frame_range[1]

                    Target = ["PERCENTAGE", self.Scale_Rate * 100, Scale_Origin, self.reverse]


                    Utility_Function.OAM_Functions.Time_Scale_Advanced(action, self.subframe, limit, Source, Target)


                    # scn.frame_start = action.frame_range[0]
                    # scn.frame_end = action.frame_range[1]


                    action_list_helper.set_active_index(index, sync=True)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Time_Scale_Selected]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
