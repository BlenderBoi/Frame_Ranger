import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


class FR_UL_Action_List(bpy.types.UIList):

    def filter_items(self, context, data, propname):
        return Utility_Function.filter_items(self, context, data, propname, "action.name")

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        preferences = Utility_Function.get_addon_preferences()

        scn = context.scene
        obj = data
        slot = item
        action = slot.action

        obj_name = obj.name

        row = layout.row(align=True)
        row.alignment="LEFT"


        if action is not None:
            settings = action.fr_settings

            row = layout.row(align=True)
            if preferences.OAM_ICON_Selection:
                row.prop(slot, "select", text="")

            if preferences.OAM_ICON_Set_Active_Slot:
                operator = row.operator("fr_oam.set_active_slot", text="", icon = "ACTION_TWEAK")
                operator.index = index
                operator.target_object = obj_name

            if preferences.OAM_ICON_Select_Object:
                operator = row.operator("fr_oam.select_object_with_action", text="", icon = "OBJECT_DATA")
                operator.index = index
                operator.target_object = obj_name
        
            if preferences.OAM_ICON_Play:
                icon = "PLAY"
                
                if context.screen.is_animation_playing:
                    if index == obj.action_list_index: 
                        icon = "PAUSE"
                    else:
                        icon = "PLAY"
                else:
                    icon= "PLAY"

                operator = row.operator("fr_oam.play_action_slot", text="", icon = icon)
                operator.index = index
                operator.target_object = obj_name
    
            if preferences.OAM_ICON_Duplicate:
                operator = row.operator("fr_oam.duplicate_action_slot", text="", icon = "DUPLICATE")
                operator.index = index
                operator.target_object = obj_name
        
            if preferences.OAM_ICON_Push_To_NLA:
                operator = row.operator("fr_oam.push_slot_action_to_nla", text="", icon = "NLA")
                operator.index = index
                operator.target_object = obj_name
                
            if preferences.OAM_ICON_Bake_This:

                operator = row.operator("fr_oam.bake_action", text="", icon = "KEYTYPE_KEYFRAME_VEC")
                operator.index = index
                operator.target_object = obj_name

            row.prop(action, "name", text="", emboss=False)

            row = layout.row(align=True)
            row.alignment = "RIGHT"
                
            if preferences.OAM_ICON_Bake_Name:
                row.prop(settings, "bake_name", text="",icon="KEYFRAME")

            if preferences.OAM_ICON_Frame_Range:

                show_normal = True 

                if preferences.ENABLE_Pose_Markers_As_Range:


                    if item.action.fr_settings.use_pose_marker_as_range:
                        show_normal = False

                        marker_a = None
                        marker_b = None

                        if item.action.fr_settings.pose_marker_a:

                            marker_a = item.action.pose_markers.get(item.action.fr_settings.pose_marker_a)
                            
                        if item.action.fr_settings.pose_marker_b:

                            marker_b = item.action.pose_markers.get(item.action.fr_settings.pose_marker_b)
                            
                        if marker_a is not None:

                            row.prop(marker_a, "frame", text="")
                        else:
                            row.separator()
                            row.prop_search(item.action.fr_settings, "pose_marker_a", item.action, "pose_markers", text="", icon="PMARKER")

                        if marker_b is not None:

                            row.prop(marker_b, "frame", text="")

                        else:
                            row.separator()
                            row.prop_search(item.action.fr_settings, "pose_marker_b", item.action, "pose_markers", text="", icon="PMARKER")





    
                if show_normal:
                    if action.use_frame_range:

                        row.prop(item.action, "use_frame_range", text="", icon="PREVIEW_RANGE")
                        row.prop(item.action, "frame_start", text="")
                        row.prop(item.action, "frame_end", text="")
                    
                    else:

                        row.prop(item.action, "use_frame_range", text="", icon="PREVIEW_RANGE")
                        row.prop(item.action, "curve_frame_range", index=0, text="")
                        row.prop(item.action, "curve_frame_range", index=1, text="")


                if preferences.ENABLE_Pose_Markers_As_Range:

                    row.prop(item.action.fr_settings, "use_pose_marker_as_range", text="", icon="PMARKER_ACT")





        
            if preferences.OAM_ICON_Cyclic:
                row.prop(action, "use_cyclic", text="", icon="FILE_REFRESH")

            if preferences.OAM_ICON_Fake_User:
                row.prop(action, "use_fake_user", text="")

            if preferences.OAM_ICON_Users:
                row.label(text=str(action.users), icon="USER")

            if preferences.OAM_ICON_Remove:
                operator = row.operator("fr_oam.remove_action_slot", text="", icon = "X")
                operator.index = index
                operator.target_object = obj_name


        else:
            # row.alignment = "LEFT"
            row.alignment = "EXPAND"
            operator = row.operator("fr_oam.remove_action_slot", text="Missing Action, Click to Remove Slot", icon = "ERROR")
            operator.index = index
            operator.target_object = obj_name



classes = [FR_UL_Action_List]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
