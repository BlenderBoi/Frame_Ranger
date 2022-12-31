import bpy
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Pose_Marker_Functions



def draw_pose_marker_range(layout, action):
    
    preferences = Utility_Function.get_addon_preferences()


    if preferences.ENABLE_Pose_Markers_As_Range:
        fr_settings = action.fr_settings

        layout.prop(fr_settings, "use_pose_marker_as_range", text="Use Pose Marker As Range")


        if fr_settings.use_pose_marker_as_range:
            marker_a = None
            marker_b = None

            if fr_settings.pose_marker_a:
                marker_a = action.pose_markers.get(fr_settings.pose_marker_a)

            if fr_settings.pose_marker_b:
                marker_b = action.pose_markers.get(fr_settings.pose_marker_b)


            box = layout.box()

            box.separator()

            box.label(text="Pose Marker A")
            row = box.row(align=True)


            if fr_settings.pose_marker_by_name:

                if marker_a:
                    row.prop(fr_settings, "pose_marker_a", text="", icon="PMARKER_ACT")
                    row.prop(marker_a, "frame", text="")




                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "A"


                else:
                    row.prop(fr_settings, "pose_marker_a", text="", icon="SORTALPHA") 


                    operator = row.operator("fr_pmm.match_marker_name_capitalization", text="", icon="SORTALPHA")
                    operator.target_action = action.name
                    operator.mode = "A"

                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "A"




            else:


                if marker_a:
                    row.prop_search(fr_settings, "pose_marker_a", action, "pose_markers", text="", icon="PMARKER_ACT")
                    row.prop(marker_a, "frame", text="")

                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "A"



                else:
                    row.prop_search(fr_settings, "pose_marker_a", action, "pose_markers", text="", icon="PMARKER") 

                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "A"


            box.label(text="Pose Marker B")
            row = box.row(align=True)


            if fr_settings.pose_marker_by_name:

                if marker_b:
                    row.prop(fr_settings, "pose_marker_b", text="", icon="PMARKER_ACT")
                    row.prop(marker_b, "frame", text="")

                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "B"


                else:

                    row.prop(fr_settings, "pose_marker_b", text="", icon="SORTALPHA") 

                    operator = row.operator("fr_pmm.match_marker_name_capitalization", text="", icon="SORTALPHA")
                    operator.target_action = action.name
                    operator.mode = "B"


                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "B"




            else:


                if marker_b:
                    row.prop_search(fr_settings, "pose_marker_b", action, "pose_markers", text="", icon="PMARKER_ACT")
                    row.prop(marker_b, "frame", text="")

                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "B"


                else:
                    row.prop_search(fr_settings, "pose_marker_b", action, "pose_markers", text="", icon="PMARKER") 

                    operator = row.operator("fr_pmm.add_pose_marker_as_range", text="", icon="ADD")
                    operator.target_action = action.name
                    operator.mode = "B"



            box.separator()

            box.prop(fr_settings, "pose_marker_by_name", text="By Name")

            operator = box.operator("fr_pmm.find_and_set_marker_as_range", text="Find Range Markers", icon="VIEWZOOM")
            operator.target_action = action.name


            box.separator()


def draw_sublist(layout, action):

    preferences = Utility_Function.get_addon_preferences()

    if Utility_Function.draw_subpanel(layout, "Pose Markers", preferences, "OAM_pmarker_Show"):
        draw_list(layout, action)


def draw_list(layout, action):

    row = layout.row()
    draw_list_box(row, action)
    draw_list_operators(row, action)

    if len(action.pose_markers) > action.pose_markers_index:
        pose_marker = action.pose_markers[action.pose_markers_index]
        layout.prop(pose_marker, "notes", text="Notes")


    draw_pose_marker_range(layout, action)


def draw_list_box(layout, action):

    layout.template_list("FR_UL_Pose_Markers_List", "", action, "pose_markers", action, "pose_markers_index")
   



def draw_list_operators(layout, action):
    
    action_name = action.name

    col = layout.column(align=True)
    operator = col.operator("fr_pmm.add_pose_marker", text="", icon = "ADD")
    operator.target_action = action_name 


    operator = col.operator("fr_pmm.remove_pose_marker", text="", icon = "REMOVE")
    operator.index = action.pose_markers_index
    operator.target_action = action_name
    
    col.separator()
    Pose_Marker_Functions.MENU_ACTION = action
    col.menu("OBJECT_MT_fr_pmm_icon_expose", text="", icon="VIS_SEL_11")
    col.menu("OBJECT_MT_fr_pmm_extra", text="", icon="DOWNARROW_HLT")
    col.separator()

    # operator = col.operator("fr_pmm.reorder_pose_marker", text="", icon = "TRIA_UP")
    # operator.index = action.pose_markers_index
    # operator.mode= "UP"
    # operator.target_action = action_name
    #
    # operator = col.operator("fr_pmm.reorder_pose_marker", text="", icon = "TRIA_DOWN")
    # operator.index = action.pose_markers_index
    # operator.mode= "DOWN"
    # operator.target_action = action_name
