
import bpy
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger import Utility_Function
from Frame_Ranger.Draw_Helper import Draw_Pose_Markers_List

MENU_OBJECT = None
ACTION_BIN_OBJECT = None



def draw_list(layout, context, obj, draw_strip, draw_action_counter):

    col = layout.column(align=True)
    row = col.row()


    if obj is not None:

        action_list_helper = OAM_Functions.Action_List_Helper(obj)
        slot = action_list_helper.get_active_slot()
        
        global ACTION_BIN_OBJECT

        ACTION_BIN_OBJECT = obj

        row.popover(panel="FR_PT_Action_Bin_Adder", text="Action Bin", icon="PLUS")
        row = col.row()

        Draw_Actions_Listbox(context, row, action_list_helper, draw_action_counter=draw_action_counter)

        col = layout.column(align=True)

        # if slot is not None:
        #
        #     action = slot.action

        if draw_strip:
            Draw_Action_Strip(context, col, action_list_helper)

       

def Draw_Actions_Listbox(context, layout, action_list_helper, draw_action_counter):

    obj = action_list_helper.obj
    obj_name = obj.name
    scn = context.scene


    col = layout.column(align=True)
    col.template_list("FR_UL_Action_List", "", obj, "action_list", obj, "action_list_index")

    if draw_action_counter:
        Draw_Action_Counter(context, col, action_list_helper)

    Draw_Actions_Listbox_Operators(context, layout, action_list_helper)


def Draw_Actions_Listbox_Operators(context, layout, action_list_helper):

    index = action_list_helper.get_active_index()

    obj = action_list_helper.obj
    obj_name = obj.name

    col = layout.column(align=True)

    operator = col.operator("fr_oam.add_action_slot", text="", icon = "ADD")
    operator.target_object = obj_name

    operator = col.operator("fr_oam.remove_action_slot", text="", icon = "REMOVE")
    operator.index = index
    operator.target_object = obj_name


    col.separator()

    global MENU_OBJECT
    MENU_OBJECT = obj

    col.menu("ACTIONLIST_MT_icon_expose", icon="VIS_SEL_11", text="")
    col.menu("ACTIONLIST_MT_extra", icon="DOWNARROW_HLT", text="")

    col.separator()
    operator = col.operator("fr_oam.reorder_action_slot", text="", icon = "TRIA_UP")
    operator.index = index 
    operator.mode = "UP"
    operator.target_object = obj_name

    operator = col.operator("fr_oam.reorder_action_slot", text="", icon = "TRIA_DOWN")
    operator.index = index 
    operator.mode = "DOWN"
    operator.target_object = obj_name



def Draw_Action_Counter(context, layout, action_list_helper):

    obj = action_list_helper.obj
    obj_name = obj.name

    objects_actions = str(action_list_helper.get_total_actions())
    all_actions = str(len(bpy.data.actions))
    
    action_display = objects_actions + " / " + all_actions + " Actions Loaded"

    layout.label(text=action_display, icon="ACTION")


def Draw_Action_Strip(context, layout, action_list_helper):

    obj = action_list_helper.obj
    obj_name = obj.name


    actual_action = action_list_helper.get_actual_action()
    active_action = action_list_helper.get_active_action()
    index = action_list_helper.get_active_index()
    slot = action_list_helper.get_active_slot()

    action_check = any([actual_action, active_action])


    if action_check:

        if actual_action == active_action:

            layout = layout.box() 
            row = layout.row(align=True)

            preferences = Utility_Function.get_addon_preferences()
            show_settings =  Utility_Function.draw_subpanel(row, "", preferences, "OAM_SHOW_Frame_Range_Settings")

            row.prop(active_action, "name", text="")

            op = row.operator("fr_oam.duplicate_action_slot", text="", icon = "DUPLICATE")
            op.index = index
            op.target_object = obj_name

            row.prop(active_action, "use_fake_user", text="")

            operator = row.operator("fr_oam.remove_action_slot", text="", icon = "X")
            operator.index = index
            operator.target_object = obj_name

            if show_settings: 
                Draw_Frame_Range_Settings(context, layout, action_list_helper, index)

                Draw_Extra_Settings(context, layout, action_list_helper, index)

                Draw_Pose_Markers_List.draw_sublist(layout, active_action)



        else:
            
            if actual_action:

                action_index = action_list_helper.find_action_index(actual_action)

                if action_index is not None:
                    row = layout.row(align=True)
                    operator = row.operator("fr_oam.set_active_slot", text="Set Active Slot", icon = "ACTION_TWEAK")
                    operator.index = action_index
                    operator.target_object = obj_name

                else:

                    if actual_action:
                        row = layout.row(align=True)
                        operator = row.operator("fr_oam.load_action_slot", text="Add Active Action", icon="ERROR")
                        operator.load_action_name= actual_action.name
                        operator.target_object = obj_name

            else:

                row = layout.row(align=True)
                op = row.operator("fr_oam.set_active_slot", text="Refresh Active", icon = "FILE_REFRESH")
                op.index = index
                op.target_object = obj_name


def Draw_Frame_Range_Settings(context, layout, action_list_helper, index):
    

    preferences = Utility_Function.get_addon_preferences()
    slot = action_list_helper.get_slot(index)

    scn = context.scene

    if slot:
        
        obj = slot.id_data
        obj_name = obj.name

        action = slot.action

        if action:

            row = layout.row(align=True)

            if action.use_frame_range:


                # if not scn.FR_TU_Autofit_Keyframe:
                #     operator = row.operator("fr_oam.set_active_slot", text="", icon="TIME")
                #     operator.index = index
                #     operator.target_object = action_list_helper.obj.name

                 

                row.prop(action, "frame_start", text="Start", index = 0)
                row.prop(action, "frame_end", text="End", index = 1)

                row.prop(action.fr_settings, "match_range_to_curve", text="" ,icon="COPYDOWN")
                row.separator()
            
                
                # row = layout.row(align=True)
                #
                # if scn.FR_TU_Autofit_Keyframe:
                #     row.operator("fr_oam.on_auto_frame_range", text="Auto Frame Range (ON)", icon="RADIOBUT_ON")
                # else:
                #     row.operator("fr_oam.on_auto_frame_range", text="Auto Frame Range (OFF)", icon="RADIOBUT_OFF")



            else:
                row.prop(action, "curve_frame_range", text="Start", index = 0)
                row.prop(action, "curve_frame_range", text="End", index = 1)

            row = layout.row(align=True)
            row.prop(action, "use_frame_range", text="Manual Frame Range")
            row = layout.row(align=True)
            row.prop(action, "use_cyclic", text="Use Cyclic")

            if preferences.ENABLE_Action_Operators:
                row = layout.row(align=True)
                operator = row.operator("fr_oam.offset_action", text="Offset", icon="PREV_KEYFRAME")
                operator.target_object = obj.name
                operator.index = index

                operator = row.operator("fr_oam.trim_action", text="Trim", icon="FIXED_SIZE")
                operator.target_object = obj.name
                operator.index = index

                operator = row.operator("fr_oam.time_scale_action", text="Timescale", icon="TIME")
                operator.target_object = obj.name
                operator.index = index



def Draw_Extra_Settings(context, layout, action_list_helper, index):

    scn = context.scene

    slot = action_list_helper.get_slot(index)

    if slot:

        action = slot.action
    
        if action:
    
            fr_settings = action.fr_settings

            show_extras_settings =  Utility_Function.draw_subpanel(layout, "Misc Settings", fr_settings, "show_extra_settings")

            if show_extras_settings:
                box = layout.box()
                box.prop(action.fr_settings, "bake_name", text="Bake Name")
                box.prop_search(fr_settings, "frame_range_set", scn, "FRM_Set", text="Frame Range Set")

