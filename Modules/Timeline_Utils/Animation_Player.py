
import bpy
from Frame_Ranger import Utility_Function


def draw_player(self, context):

    preferences = Utility_Function.get_addon_preferences()


    if preferences.TU_Animation_Player:

        layout = self.layout
        scene = context.scene
        tool_settings = context.tool_settings
        screen = context.screen

        if context.area.ui_type == "DOPESHEET":
            # if context.space_data.ui_mode == 'ACTION' or context.space_data.ui_mode == 'SHAPEKEY' or context.space_data.ui_mode == 'GPENCIL':
            # if context.space_data.ui_mode == 'CACHEFILE':


            if False:

                row = layout.row(align=True)


                row.prop(tool_settings, "use_keyframe_insert_auto", text="", toggle=True)
                sub = row.row(align=True)
                sub.active = tool_settings.use_keyframe_insert_auto
                sub.popover(
                    panel="TIME_PT_auto_keyframing_Dopesheet",
                    text="",
                )



            else:
                layout.separator_spacer()

                row = layout.row(align=True)


                row.prop(tool_settings, "use_keyframe_insert_auto", text="", toggle=True)
                sub = row.row(align=True)
                sub.active = tool_settings.use_keyframe_insert_auto
                sub.popover(
                    panel="TIME_PT_auto_keyframing_Dopesheet",
                    text="",
                )

                row = layout.row(align=True)
                row.operator("screen.frame_jump", text="", icon='REW').end = False
                row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
                if not screen.is_animation_playing:
                    # if using JACK and A/V sync:
                    #   hide the play-reversed button
                    #   since JACK transport doesn't support reversed playback
                    if scene.sync_mode == 'AUDIO_SYNC' and context.preferences.system.audio_device == 'JACK':
                        row.scale_x = 2
                        row.operator("screen.animation_play", text="", icon='PLAY')
                        row.scale_x = 1
                    else:
                        row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
                        row.operator("screen.animation_play", text="", icon='PLAY')
                else:
                    row.scale_x = 2
                    row.operator("screen.animation_play", text="", icon='PAUSE')
                    row.scale_x = 1
                row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
                row.operator("screen.frame_jump", text="", icon='FF').end = True


        else:
            layout.separator_spacer()

            row = layout.row(align=True)
            row.prop(tool_settings, "use_keyframe_insert_auto", text="", toggle=True)
            sub = row.row(align=True)
            sub.active = tool_settings.use_keyframe_insert_auto
            sub.popover(
                panel="TIME_PT_auto_keyframing_Dopesheet",
                text="",
            )

            row = layout.row(align=True)
            row.operator("screen.frame_jump", text="", icon='REW').end = False
            row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
            if not screen.is_animation_playing:
                # if using JACK and A/V sync:
                #   hide the play-reversed button
                #   since JACK transport doesn't support reversed playback
                if scene.sync_mode == 'AUDIO_SYNC' and context.preferences.system.audio_device == 'JACK':
                    row.scale_x = 2
                    row.operator("screen.animation_play", text="", icon='PLAY')
                    row.scale_x = 1
                else:
                    row.operator("screen.animation_play", text="", icon='PLAY_REVERSE').reverse = True
                    row.operator("screen.animation_play", text="", icon='PLAY')
            else:
                row.scale_x = 2
                row.operator("screen.animation_play", text="", icon='PAUSE')
                row.scale_x = 1
            row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
            row.operator("screen.frame_jump", text="", icon='FF').end = True


def draw_frame_range(self, context):
    preferences = Utility_Function.get_addon_preferences()
    if preferences.TU_Frame_Range:
        layout = self.layout
        scene = context.scene
        tool_settings = context.tool_settings
        screen = context.screen

        # layout.separator_spacer()
        if not context.area.ui_type == "TIMELINE":
            row = layout.row()
            if scene.show_subframe:
                row.scale_x = 1.15
                row.prop(scene, "frame_float", text="")
            else:
                row.scale_x = 0.95
                row.prop(scene, "frame_current", text="")

            row = layout.row(align=True)
            row.prop(scene, "use_preview_range", text="", toggle=True)
            sub = row.row(align=True)
            sub.scale_x = 0.8
            if not scene.use_preview_range:
                sub.prop(scene, "frame_start", text="Start")
                sub.prop(scene, "frame_end", text="End")
            else:
                sub.prop(scene, "frame_preview_start", text="Start")
                sub.prop(scene, "frame_preview_end", text="End")

class DopesheetButtons:
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'


class TIME_PT_auto_keyframing_Dopesheet(DopesheetButtons, bpy.types.Panel):
    bl_label = "Auto Keyframing"
    bl_options = {'HIDE_HEADER'}
    bl_region_type = 'HEADER'
    bl_ui_units_x = 9



    def draw(self, context):
        layout = self.layout

        tool_settings = context.tool_settings
        prefs = context.preferences

        layout.active = tool_settings.use_keyframe_insert_auto

        layout.prop(tool_settings, "auto_keying_mode", expand=True)

        col = layout.column(align=True)
        col.prop(tool_settings, "use_keyframe_insert_keyingset", text="Only Active Keying Set", toggle=False)
        if not prefs.edit.use_keyframe_insert_available:
            col.prop(tool_settings, "use_record_with_nla", text="Layered Recording")

        col.prop(tool_settings, "use_keyframe_cycle_aware")


def Add_Player():
    bpy.types.DOPESHEET_MT_editor_menus.append(draw_player)
    bpy.types.DOPESHEET_HT_header.append(draw_frame_range)

    bpy.types.GRAPH_MT_editor_menus.append(draw_player)
    bpy.types.GRAPH_HT_header.append(draw_frame_range)

    bpy.types.NLA_MT_editor_menus.append(draw_player)
    bpy.types.NLA_HT_header.append(draw_frame_range)

    bpy.types.SEQUENCER_MT_editor_menus.append(draw_player)
    bpy.types.SEQUENCER_HT_header.append(draw_frame_range)

def Remove_Player():
    bpy.types.DOPESHEET_MT_editor_menus.remove(draw_player)
    bpy.types.DOPESHEET_HT_header.remove(draw_frame_range)

    bpy.types.GRAPH_MT_editor_menus.remove(draw_player)
    bpy.types.GRAPH_HT_header.remove(draw_frame_range)

    bpy.types.NLA_MT_editor_menus.remove(draw_player)
    bpy.types.NLA_HT_header.remove(draw_frame_range)

    bpy.types.SEQUENCER_MT_editor_menus.remove(draw_player)
    bpy.types.SEQUENCER_HT_header.remove(draw_frame_range)


def register():
    bpy.utils.register_class(TIME_PT_auto_keyframing_Dopesheet)
    Add_Player()

def unregister():
    bpy.utils.unregister_class(TIME_PT_auto_keyframing_Dopesheet)
    Remove_Player()


if __name__ == "__main__":
    register()
