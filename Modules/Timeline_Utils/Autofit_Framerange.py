import bpy

from bpy.app.handlers import persistent
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

@ persistent
def load_setting(scene):

    if bpy.context.scene.FR_TU_Autofit_Keyframe:
        bpy.context.scene.FR_TU_Autofit_Keyframe = True





@persistent
def handler_fit_keyframe(scene):

    scn = bpy.context.scene

    preferences = Utility_Function.get_addon_preferences()


    if scn.FR_TU_Auto_Frame_Range_Settings.Mode == "ACTION":

        if scn.FR_TU_Auto_Frame_Range_Settings.Selected:
            objects = bpy.context.selected_objects
        else:
            objects = scn.objects

        ranges_start = []
        ranges_end = []

        for obj in objects:
            

            action_list_helper=  OAM_Functions.Action_List_Helper(obj)

            if obj.animation_data:

                act = action_list_helper.get_active_action()

                # act = obj.animation_data.action

                if not act:
                    act = action_list_helper.get_actual_action()


                if act:


                    fr_settings = act.fr_settings

                    use_curve_range = False

                    if scn.FR_TU_Auto_Frame_Range_Settings.Action_Mode == "KEYFRAME":
                        use_curve_range = True

                    if scn.FR_TU_Auto_Frame_Range_Settings.Action_Mode == "ACTION":
                        use_curve_range = False


                    frame_ranges = action_list_helper.get_action_frame_range(act, use_curve_range=use_curve_range)

                    start = frame_ranges[0]
                    end = frame_ranges[1]



                    if start is not None and end is not None:
                        ranges_start.append(start)
                        ranges_end.append(end)




        if len(ranges_start) > 0:
            scn.frame_start = int(min(ranges_start))
        if len(ranges_end) > 0:
            scn.frame_end = int(max(ranges_end))




    if scn.FR_TU_Auto_Frame_Range_Settings.Mode == "NLA":

        ranges_start = []
        ranges_end = []

        objects = scn.objects
        for object in objects:

            if object.animation_data:
                if object.animation_data.nla_tracks:
                    for track in object.animation_data.nla_tracks:
                        if track.strips:
                            for strip in track.strips:
                                if scn.FR_TU_Auto_Frame_Range_Settings.Selected:
                                    if strip.select:

                                        ranges_start.append(strip.frame_start)
                                        ranges_end.append(strip.frame_end+1)
                                else:
                                    ranges_start.append(strip.frame_start)
                                    ranges_end.append(strip.frame_end+1)

        if len(ranges_start) > 0:
            scn.frame_start = int(min(ranges_start))
        if len(ranges_end) > 0:
            scn.frame_end = int(max(ranges_end) -1)


    if scn.FR_TU_Auto_Frame_Range_Settings.Mode == "SEQUENCE":

        list_end = []
        list_start = []


        for sequence in bpy.context.sequences:

            if scn.FR_TU_Auto_Frame_Range_Settings.Selected:
                if sequence.select:
                    list_start.append(sequence.frame_final_start)
                    list_end.append(sequence.frame_final_end)
            else:

                list_start.append(sequence.frame_final_start)
                list_end.append(sequence.frame_final_end)



        if len(list_start) > 0:
            scn.frame_start = int(min(list_start))
        if len(list_end) > 0:
            scn.frame_end = int(max(list_end) -1)






def autofit_keyframe(self, context):

    scn = context.scene

    if context.area:
        if context.area.ui_type == "SEQUENCE_EDITOR":
            scn.FR_TU_Auto_Frame_Range_Settings.Mode = "SEQUENCE"

        if context.area.ui_type == "NLA_EDITOR":
            scn.FR_TU_Auto_Frame_Range_Settings.Mode = "NLA"

    if context.scene.FR_TU_Autofit_Keyframe:
        bpy.app.handlers.depsgraph_update_post.append(handler_fit_keyframe)
        # context.scene.Autofit_Sequence = False



    if context.scene.FR_TU_Autofit_Keyframe == False:
        if handler_fit_keyframe in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(handler_fit_keyframe)

    # try:
    #     if context.scene.FR_TU_Autofit_Keyframe == False:
    #
    #         bpy.app.handlers.depsgraph_update_post.remove(handler_fit_keyframe)
    # except:
    #     print("Fail to Remove Handlers") 

    if scn.FR_TU_Autofit_Keyframe:
        handler_fit_keyframe(context)


def draw_item_keyframe(self, context):

    preferences = Utility_Function.get_addon_preferences()

    if preferences.TU_Auto_Frame_Range:

        layout = self.layout
        layout.separator()
        layout.prop(context.scene, "FR_TU_Autofit_Keyframe", text="", icon="TIME")
        # layout.menu("FR_TU_auto_frame_range", text="", icon="TRIA_DOWN")

        layout.popover(
            panel="FR_PT_TU_auto_frame_range",
            text="",
        )





class FR_PT_TU_Auto_Frame_Range(bpy.types.Panel):
    bl_label = "Auto Frame Range"
    bl_idname = "FR_PT_TU_auto_frame_range"
    bl_options = {'HIDE_HEADER'}
    bl_region_type = 'HEADER'
    bl_space_type = 'DOPESHEET_EDITOR'



    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Mode", text="Mode", expand=True)
        if scn.FR_TU_Auto_Frame_Range_Settings.Mode == "ACTION":
            layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Action_Mode", text="Only Selected", expand=True)


        layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Selected", text="Only Selected")


        preferences = Utility_Function.get_addon_preferences()

        if preferences.ENABLE_Pose_Markers_As_Range:
            layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Use_Pose_Marker_As_Range", text="Use Pose Marker As Range")





Mode = [("ACTION","Action","Action"),("NLA","NLA","NLA Strips"),("SEQUENCE","Sequence","Sequencer Strips")]
# Mode = [("ACTION","Action","Action"),("NLA","NLA","NLA Strips"),("SEQUENCE","Sequence","Sequencer Strips")]
Action_Mode = [("ACTION","Settings","Settings"), ("KEYFRAME","Keyframe","Keyframe")]


class FR_TU_Auto_Frame_Range_Settings(bpy.types.PropertyGroup):

    Mode : bpy.props.EnumProperty(items=Mode, default="ACTION")
    Action_Mode : bpy.props.EnumProperty(items=Action_Mode, default="ACTION")
    Selected: bpy.props.BoolProperty(default=False)

    Use_Pose_Marker_As_Range: bpy.props.BoolProperty(default=False)




classes = [
        FR_TU_Auto_Frame_Range_Settings,
        FR_PT_TU_Auto_Frame_Range
        ]








def register():
    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Scene.FR_TU_Autofit_Keyframe = bpy.props.BoolProperty(default=False, update=autofit_keyframe)
    bpy.types.Scene.FR_TU_Auto_Frame_Range_Settings = bpy.props.PointerProperty(type=FR_TU_Auto_Frame_Range_Settings)



    bpy.types.TIME_MT_editor_menus.append(draw_item_keyframe)
    bpy.types.DOPESHEET_MT_editor_menus.append(draw_item_keyframe)
    bpy.types.GRAPH_MT_editor_menus.append(draw_item_keyframe)
    bpy.types.NLA_MT_editor_menus.append(draw_item_keyframe)
    bpy.types.SEQUENCER_MT_editor_menus.append(draw_item_keyframe)

    bpy.app.handlers.load_post.append(load_setting)




def unregister():

    if handler_fit_keyframe in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(handler_fit_keyframe)


    for cls in classes:
        bpy.utils.unregister_class(cls)


    bpy.app.handlers.load_post.remove(load_setting)


    bpy.types.TIME_MT_editor_menus.remove(draw_item_keyframe)
    bpy.types.DOPESHEET_MT_editor_menus.remove(draw_item_keyframe)
    bpy.types.GRAPH_MT_editor_menus.remove(draw_item_keyframe)
    bpy.types.NLA_MT_editor_menus.remove(draw_item_keyframe)
    bpy.types.SEQUENCER_MT_editor_menus.remove(draw_item_keyframe)


    del bpy.types.Scene.FR_TU_Autofit_Keyframe
    del bpy.types.Scene.FR_TU_Auto_Frame_Range_Settings


if __name__ == "__main__":
    register()
