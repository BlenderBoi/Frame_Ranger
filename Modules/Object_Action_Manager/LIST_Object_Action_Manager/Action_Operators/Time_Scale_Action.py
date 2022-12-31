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

class FR_OT_OAM_Time_Scale_Action(bpy.types.Operator):
    bl_idname = "fr_oam.time_scale_action"
    bl_label = "Time Scale Action"
    bl_description = "Time Scale Action"
    bl_options = {"REGISTER", "UNDO"}

    index: bpy.props.IntProperty()
    target_object: bpy.props.StringProperty()

    Scale_Mode: bpy.props.EnumProperty(items=Scale_Mode, default="REMAP")
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
    
        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.set_active_index(self.index)
            
            action = action_list_helper.get_action(self.index)

            frame_range = action_list_helper.get_slot_frame_range_by_index(self.index)

            start = int(frame_range[0])
            end = int(frame_range[1])

            self.start = start
            self.end = end 

            self.src_start = start 
            self.src_end = end

            scn.frame_start = start 
            scn.frame_end = end 

            self.Scale_Origin = start

            scn.frame_current = scn.frame_start

            return context.window_manager.invoke_props_dialog(self)


        return {'FINISHED'}


    def draw(self, context):

        scn = context.scene

        layout = self.layout.column(align=True)
        row = layout.row(align=True)

        scn = context.scene


        row = layout.row(align=True)
        row.prop(self, "Scale_Mode", text="", icon="UV_SYNC_SELECT")
        row = layout.row(align=True)
        if self.Scale_Mode == "RATE":

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


        if self.Scale_Mode == "REMAP":
            row = layout.row(align=True)
            row.prop(self, "sync_range", text="", icon="UV_SYNC_SELECT")

            if self.sync_range:
                row.prop(scn, "frame_start", text="")
                row.prop(scn, "frame_end", text="")
                row = layout.row(align=True)

            else:
                row.prop(self, "start", text="")
                row.prop(self, "end", text="")
                row = layout.row(align=True)

        layout.separator()
        row = layout.row(align=True)

        row.prop(self, "subframe", text="Subframe")
        row.prop(self, "reverse", text="Reverse")
        # row.prop(self, "Limit_Mode", text="Limit Mode")
        # layout.separator()
        layout.separator()

    def execute(self, context):



        obj = bpy.data.objects.get(self.target_object)
        scn = context.scene

        if self.sync_range:
            self.start = scn.frame_start
            self.end = scn.frame_end
    
        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.set_active_index(self.index)


            if self.sync_origin:
                self.Scale_Origin = scn.frame_current


            action = action_list_helper.get_action(self.index)
            frame_range = action_list_helper.get_slot_frame_range_by_index(self.index)



            if self.reverse:
                store_end = self.start
                store_start = self.end
            else:
                store_start = self.start
                store_end = self.end


            if self.Scale_Mode == "REMAP":

                limit = self.Limit_Mode
                Source = [self.src_start, self.src_end]
                Target = ["REMAP",store_start, store_end, self.reverse]
                OAM_Functions.Time_Scale_Advanced(action, self.subframe, limit, Source, Target)
                 







            if self.Scale_Mode == "RATE":
                limit = self.Limit_Mode
                Source = [self.src_start, self.src_end]




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




            action_list_helper.set_active_index(self.index, sync=True)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Time_Scale_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
