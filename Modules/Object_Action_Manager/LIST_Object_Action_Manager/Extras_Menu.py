import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Draw_Helper import Draw_Action_List



def draw_operators(self, context, obj):

    preferences = Utility_Function.get_addon_preferences()

    scn = context.scene

    obj_name = obj.name
    index = obj.action_list_index

    layout = self.layout

    operator = layout.operator("fr_oam.import_fbx_action", text="Import And Load FBX Actions" ,icon="IMPORT")
    operator.load_to_object= True 
    operator.target_object = obj_name

    layout.separator()

    operator = layout.operator("fr_oam.recursive_import_fbx_action", text="Recursive Import And Load FBX Actions (Experimental)" ,icon="IMPORT")
    operator.load_to_object= True 
    operator.target_object = obj_name

    layout.separator()


    operator = layout.operator("fr_oam.choose_and_append_blendfile_action", text="Choose and Append Blend File Action" ,icon="FILE_BLEND")
    operator.load_to_object= True
    operator.target_object = obj_name
    
    operator = layout.operator("fr_oam.append_all_actions_from_blendfiles", text="Append All Actions from Multiple Blend Files" ,icon="FILE_BLEND")
    operator.load_to_object= True
    operator.target_object = obj_name
     
    layout.separator()

    operator = layout.operator("fr_oam.load_all_action", text="Load Multiple Actions" ,icon="ACTION")
    operator.target_object = obj_name
    operator.filter = preferences.ABA_Filter
    operator.filter_mode = preferences.ABA_Filter_Mode
    operator.show_options = True


    operator = layout.operator("fr_oam.load_action_slot", text="Load Single Action" ,icon="ACTION_TWEAK")
    operator.target_object = obj_name
    operator.show_options = True

    layout.separator()

    operator = layout.operator("fr_oam.push_all_to_nla", text="Push All to NLA" ,icon="NLA")
    operator.target_object = obj_name

    layout.separator()

    operator = layout.operator("fr_oam.batch_rename_actions", text="Batch Rename Actions" ,icon="SORTALPHA")
    operator.target_object = obj_name

    operator = layout.operator("fr_oam.sort_action_slot", text="Sort Action Slot" ,icon="SORTALPHA")
    operator.target_object = obj_name

    layout.separator()
    
    operator = layout.operator("fr_oam.clear_action_list", text="Clear List" ,icon="TRASH")
    operator.target_object = obj_name
    
    op = layout.operator("fr_oam.remove_by_condition", text="Remove By Condition" ,icon="TRASH")
    op.target_object = obj_name

    op = layout.operator("fr_oam.clean_action_list", text="Clean List" ,icon="BRUSH_DATA")
    op.target_object = obj_name

    layout.separator()
    #
    operator = layout.operator("fr_oam.toogle_fake_users", text="Fake User On" ,icon="FAKE_USER_ON")
    operator.target_object = obj_name
    operator.fake_user = True

    operator = layout.operator("fr_oam.toogle_fake_users", text="Fake User Off" ,icon="FAKE_USER_OFF")
    operator.target_object = obj_name
    operator.fake_user = False
    layout.separator()

    operator = layout.operator("fr_oam.bake_selected_action", text="Bake Selected Actions" ,icon="KEYTYPE_KEYFRAME_VEC")
    operator.target_object = obj_name

    operator = layout.operator("fr_oam.duplicate_and_replace_all_slot", text="Duplicate And Replace All Slot" ,icon="DUPLICATE")
    operator.target_object = obj_name



    if preferences.ENABLE_Pose_Markers_As_Range:
        layout.separator()
        operator = layout.operator("fr_oam.find_all_actions_range_markers", text="Find And Set All Action's Range Markers" ,icon="VIEWZOOM")
        operator.target_object = obj_name


    if preferences.ENABLE_Action_Operators:
        layout.separator()
        operator = layout.operator("fr_oam.offset_selected", text="Offset Selected", icon="PREV_KEYFRAME")
        operator.target_object = obj_name

        operator = layout.operator("fr_oam.trim_selected", text="Trim Selected", icon="FIXED_SIZE")
        operator.target_object = obj_name

        operator = layout.operator("fr_oam.time_scale_selected", text="Timescale Selected", icon="TIME")
        operator.target_object = obj_name

class FR_MT_Action_List_Extra_Menu(bpy.types.Menu):
    bl_label = "Action List Extras Menu"
    bl_idname = "ACTIONLIST_MT_extra"

    def draw(self, context):


        obj = Draw_Action_List.MENU_OBJECT
        draw_operators(self, context, obj)



class FR_MT_Action_List_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Action List Icon Expose Menu"
    bl_idname = "ACTIONLIST_MT_icon_expose"

    def draw(self, context):

        scn = context.scene

        preferences = Utility_Function.get_addon_preferences()

        options = [
            ("OAM_ICON_Selection", "Selection", None),                          #
            ("OAM_ICON_Set_Active_Slot", "Set Active Slot", "ACTION_TWEAK"),    #
            ("OAM_ICON_Play", "Play", "PLAY"),                                  #
            ("OAM_ICON_Select_Object", "Select Object", "OBJECT_DATA"),         #
            ("OAM_ICON_Duplicate", "Duplicate", "DUPLICATE"),                   #
            ("OAM_ICON_Push_To_NLA", "Push To NLA", "NLA"),                     #
            ("OAM_ICON_Bake_This", "Bake Action", "KEYTYPE_KEYFRAME_VEC"),                     #
            ("OAM_ICON_Bake_Name", "Bake Name", None),                      #
            ("OAM_ICON_Frame_Range", "Frame Range", None),                      #
            ("OAM_ICON_Cyclic","Use Cyclic","FILE_REFRESH"),                    #
            ("OAM_ICON_Fake_User", "Fake User", "FAKE_USER_ON"),                #
            ("OAM_ICON_Users", "Users", "USER"),                                #
            ("OAM_ICON_Remove", "Remove Slot", "X"),                            #
        ]

        layout = self.layout

        for option in options:
            
            if option[2]:
                row = layout.row(align=True)
                row.label(text="", icon=option[2])
                row.prop(preferences, option[0], text=option[1], icon=option[2])
                row.separator()
            else:
                row = layout.row(align=True)
                row.label(text="", icon="DOT")
                row.prop(preferences, option[0], text=option[1])
                row.separator()



classes = [FR_MT_Action_List_Extra_Menu, FR_MT_Action_List_Icon_Expose_Menu]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
