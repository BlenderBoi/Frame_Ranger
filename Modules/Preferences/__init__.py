from Frame_Ranger import Utility_Function

import bpy
import os
import pathlib
from bpy.types import Object
import rna_keymap_ui
from . import keymaps

addon_name = __package__.split(".")[0]


def append_panel_class(panels, cls, category, label):
    panel = cls 
    item = [panel, category, label]
    panels.append(item)

    return panels

def append_panel_module(panels, module, category, label):

    for cls in module.classes:
        if isinstance(cls, type):
            panels = append_panel_class(panels, cls, category, label)
    
    return panels


def unregister_panel(context):

    addon_preferences = Utility_Function.get_addon_preferences()
    
    message = ": Unregistering Panel failed"

    panels = []

    from Frame_Ranger.Modules import Object_Action_Manager

    panel_module = Object_Action_Manager.Panels
    category = addon_preferences.PANEL_Object_Action_Manager_Category
    label = addon_preferences.PANEL_Object_Action_Manager_Label
    panels = append_panel_module(panels, panel_module, category, label) 



    from Frame_Ranger.Modules import Action_Baker

    panel_module = Action_Baker.Panels
    category = addon_preferences.PANEL_Action_Baker_Category
    label = addon_preferences.PANEL_Action_Baker_Label
    panels = append_panel_module(panels, panel_module, category, label) 


    from Frame_Ranger.Modules import Action_Bin 

    panel_module = Action_Bin.Panels
    category = addon_preferences.PANEL_Action_Bin_Category
    label = addon_preferences.PANEL_Action_Bin_Label
    panels = append_panel_module(panels, panel_module, category, label) 


    from Frame_Ranger.Modules import Frame_Range_Manager 

    panel_module = Frame_Range_Manager.Panels
    category = addon_preferences.PANEL_Frame_Range_Manager_Category
    label = addon_preferences.PANEL_Frame_Range_Manager_Label
    panels = append_panel_module(panels, panel_module, category, label) 


    from Frame_Ranger.Modules import Timeline_Marker_Manager

    panel_module = Timeline_Marker_Manager.Panels
    category = addon_preferences.PANEL_Timeline_Marker_Manager_Category
    label = addon_preferences.PANEL_Timeline_Marker_Manager_Label
    panels = append_panel_module(panels, panel_module, category, label) 



    from Frame_Ranger.Modules import Timeline_Utils

    panel_module = Timeline_Utils.Panels
    category = addon_preferences.PANEL_Frame_Remapper_Category
    label = addon_preferences.PANEL_Frame_Remapper_Label
    panels = append_panel_module(panels, panel_module, category, label) 

    try:
        for item in panels:

            panel = item[0]
            category = item[1]
            label = item[2]
           
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass






def update_panel(self, context):

    addon_preferences = Utility_Function.get_addon_preferences()
    
    message = ": Updating Panel locations has failed"

    panels = []

    from Frame_Ranger.Modules import Object_Action_Manager

    panel_module = Object_Action_Manager.Panels
    category = addon_preferences.PANEL_Object_Action_Manager_Category
    label = addon_preferences.PANEL_Object_Action_Manager_Label
    panels = append_panel_module(panels, panel_module, category, label) 



    from Frame_Ranger.Modules import Action_Baker

    panel_module = Action_Baker.Panels
    category = addon_preferences.PANEL_Action_Baker_Category
    label = addon_preferences.PANEL_Action_Baker_Label
    panels = append_panel_module(panels, panel_module, category, label) 


    from Frame_Ranger.Modules import Action_Bin 

    panel_module = Action_Bin.Panels
    category = addon_preferences.PANEL_Action_Bin_Category
    label = addon_preferences.PANEL_Action_Bin_Label
    panels = append_panel_module(panels, panel_module, category, label) 


    from Frame_Ranger.Modules import Frame_Range_Manager 

    panel_module = Frame_Range_Manager.Panels
    category = addon_preferences.PANEL_Frame_Range_Manager_Category
    label = addon_preferences.PANEL_Frame_Range_Manager_Label
    panels = append_panel_module(panels, panel_module, category, label) 


    from Frame_Ranger.Modules import Timeline_Marker_Manager

    panel_module = Timeline_Marker_Manager.Panels
    category = addon_preferences.PANEL_Timeline_Marker_Manager_Category
    label = addon_preferences.PANEL_Timeline_Marker_Manager_Label
    panels = append_panel_module(panels, panel_module, category, label) 



    from Frame_Ranger.Modules import Timeline_Utils

    panel_module = Timeline_Utils.Panels
    category = addon_preferences.PANEL_Frame_Remapper_Category
    label = addon_preferences.PANEL_Frame_Remapper_Label
    panels = append_panel_module(panels, panel_module, category, label) 

    try:
        pass
        for item in panels:

            panel = item[0]
            category = item[1]
            label = item[2]
           
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)


            panel.bl_category = category
            panel.bl_label = label
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass



ENUM_Tabs = [("PANELS", "Panels", "Panels"),("GENERAL", "General", "General") , ("KEYMAPS","Keymaps","Keymaps")]

ENUM_filter_mode = [("INCLUDE","Include","Include"),("EXCLUDE","Exclude","Exclude")]



class FR_Preferences(bpy.types.AddonPreferences):

    bl_idname = addon_name 

    TABS_Preferences: bpy.props.EnumProperty(items=ENUM_Tabs)

    
    PANEL_Object_Action_Manager: bpy.props.BoolProperty(default=True)
    PANEL_Object_Action_Manager_Category: bpy.props.StringProperty(default="Action Manager", update=update_panel)
    PANEL_Object_Action_Manager_Label: bpy.props.StringProperty(default="Object Action Manager", update=update_panel)
    
    PANEL_Timeline_Marker_Manager: bpy.props.BoolProperty(default=True)
    PANEL_Timeline_Marker_Manager_Category: bpy.props.StringProperty(default="Frame Ranger", update=update_panel)
    PANEL_Timeline_Marker_Manager_Label: bpy.props.StringProperty(default="Timeline Marker Manager", update=update_panel)

    PANEL_Action_Bin: bpy.props.BoolProperty(default=True)
    PANEL_Action_Bin_Category: bpy.props.StringProperty(default="Action Manager", update=update_panel)
    PANEL_Action_Bin_Label: bpy.props.StringProperty(default="Action Bin", update=update_panel)

    PANEL_Action_Bin_Side_Panel: bpy.props.BoolProperty(default=False)
    PANEL_Action_Bin_Scene_Properties_Panel: bpy.props.BoolProperty(default=True)

    PANEL_Action_Baker: bpy.props.BoolProperty(default=True)
    PANEL_Action_Baker_Category: bpy.props.StringProperty(default="Action Manager", update=update_panel)
    PANEL_Action_Baker_Label: bpy.props.StringProperty(default="Action Baker", update=update_panel)
    PANEL_Action_Baker_Show_Action_Selector: bpy.props.BoolProperty(default=True)


    PANEL_Frame_Range_Manager: bpy.props.BoolProperty(default=True)
    PANEL_Frame_Range_Manager_Category: bpy.props.StringProperty(default="Frame Ranger", update=update_panel)
    PANEL_Frame_Range_Manager_Label: bpy.props.StringProperty(default="Frame Range Manager", update=update_panel)


    PANEL_Frame_Remapper: bpy.props.BoolProperty(default=True)
    PANEL_Frame_Remapper_Category: bpy.props.StringProperty(default="Frame Ranger", update=update_panel)
    PANEL_Frame_Remapper_Label: bpy.props.StringProperty(default="Frame Remapper", update=update_panel)

    PANEL_Frame_Remapper_Output_Properties_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Frame_Remapper_Side_Panel: bpy.props.BoolProperty(default=False)



    MM_View_Move_To: bpy.props.BoolProperty(default=True)

    OAM_FR_Update_Active_Action: bpy.props.BoolProperty(default=True)
    # Object Action Manager Icons
   
    ABA_Filter: bpy.props.StringProperty(options={'TEXTEDIT_UPDATE'})

    ABA_Filter_Mode: bpy.props.EnumProperty(items=ENUM_filter_mode)

    OAM_ICONEXPOSE_Show: bpy.props.BoolProperty(default=False)
    OAM_ICON_Remove: bpy.props.BoolProperty(default=True)
    OAM_ICON_Fake_User: bpy.props.BoolProperty(default=True)
    OAM_ICON_Duplicate: bpy.props.BoolProperty(default=False)
    OAM_ICON_Play: bpy.props.BoolProperty(default=False)
    OAM_ICON_Users: bpy.props.BoolProperty(default=False)
    OAM_ICON_Frame_Range: bpy.props.BoolProperty(default=False)
    OAM_ICON_Select_Object: bpy.props.BoolProperty(default=False)
    OAM_ICON_Set_Active_Slot: bpy.props.BoolProperty(default=False)
    OAM_ICON_Selection: bpy.props.BoolProperty(default=True)
    OAM_ICON_Cyclic: bpy.props.BoolProperty(default=False)
    OAM_ICON_Push_To_NLA: bpy.props.BoolProperty(default=False)
    OAM_ICON_Bake_Name: bpy.props.BoolProperty(default=False)
    OAM_ICON_Bake_This: bpy.props.BoolProperty(default=False)

    OAM_pmarker_Show: bpy.props.BoolProperty(default=False)
    OAM_pmarker_ICONEXPOSE_Show: bpy.props.BoolProperty(default=False)
    OAM_pmarker_ICON_Move_To: bpy.props.BoolProperty(default=True)
    OAM_pmarker_ICON_Selection: bpy.props.BoolProperty(default=False)
    OAM_pmarker_ICON_Frame: bpy.props.BoolProperty(default=True)
    OAM_pmarker_ICON_Camera: bpy.props.BoolProperty(default=False)
    OAM_pmarker_ICON_Remove: bpy.props.BoolProperty(default=True)

    ENABLE_Pose_Markers_As_Range: bpy.props.BoolProperty(default=False)

    OAM_tmarker_Show: bpy.props.BoolProperty(default=False)
    OAM_tmarker_ICONEXPOSE_Show: bpy.props.BoolProperty(default=False)
    OAM_tmarker_ICON_Move_To: bpy.props.BoolProperty(default=True)
    OAM_tmarker_ICON_Selection: bpy.props.BoolProperty(default=False)
    OAM_tmarker_ICON_Frame: bpy.props.BoolProperty(default=True)
    OAM_tmarker_ICON_Camera: bpy.props.BoolProperty(default=False)
    OAM_tmarker_ICON_Remove: bpy.props.BoolProperty(default=True)


    OAM_Pose_Marker_Warning: bpy.props.BoolProperty(default=True) 
    OAM_Timeline_Marker_Warning: bpy.props.BoolProperty(default=True) 

    OAM_SHOW_Frame_Range_Settings: bpy.props.BoolProperty(default=True)
    OAM_SHOW_Action_Bin_Settings: bpy.props.BoolProperty(default=True)


    AB_ICON_Select_Object: bpy.props.BoolProperty(default=False)
    AB_ICON_Load_Action_To_Object: bpy.props.BoolProperty(default=True)
    AB_ICON_Fake_User: bpy.props.BoolProperty(default=True)
    AB_ICON_Duplicate: bpy.props.BoolProperty(default=True)
    AB_ICON_Users: bpy.props.BoolProperty(default=True)
    AB_ICON_Remove: bpy.props.BoolProperty(default=True)


    FRM_ICON_Set_Range: bpy.props.BoolProperty(default=True)
    FRM_ICON_Frame_Range: bpy.props.BoolProperty(default=True)
    FRM_ICON_Remove: bpy.props.BoolProperty(default=True)

    FRS_ICON_Remove: bpy.props.BoolProperty(default=True)



    BAKER_ICON_Duplicate: bpy.props.BoolProperty(default=False)
    BAKER_ICON_Frame_Range: bpy.props.BoolProperty(default=False)
    BAKER_ICON_Bake_Name: bpy.props.BoolProperty(default=True)
    BAKER_ICON_REMOVE: bpy.props.BoolProperty(default=False)
    BAKER_ICON_Set_Active_Slot: bpy.props.BoolProperty(default=False)

    BAKER_ICON_Fake_User: bpy.props.BoolProperty(default=False)
    BAKER_ICON_Users: bpy.props.BoolProperty(default=False)

    TU_Animation_Player: bpy.props.BoolProperty(default=True)
    TU_Frame_Range: bpy.props.BoolProperty(default=True)
    TU_Auto_Frame_Range: bpy.props.BoolProperty(default=True)


    SHOW_IO_Frame_Range: bpy.props.BoolProperty(default=True)
    SHOW_IO_Timeline_Markers: bpy.props.BoolProperty(default=True)

    ENABLE_Action_Operators: bpy.props.BoolProperty(default=False)


    # OAM_ICON_isBake: bpy.props.BoolProperty(default=False)
    # OAM_ICON_Bake: bpy.props.BoolProperty(default=False)
    # OAM_ICON_Timescale: bpy.props.BoolProperty(default=False)
    # OAM_ICON_Trim: bpy.props.BoolProperty(default=False)
    # OAM_ICON_Offset: bpy.props.BoolProperty(default=False)

    def draw_panel_options(self, context, layout):
         
        col = layout.column(align=True)

        col.separator()

        col.label(text="Panels")

        col.separator()
        col.separator()
        col.separator()





        col.prop(self, "PANEL_Frame_Range_Manager", text="Frame Range Manager Panel")

        if self.PANEL_Frame_Range_Manager:
            box = col.box()
            box.prop(self, "PANEL_Frame_Range_Manager_Category", text="Category")
            box.prop(self, "PANEL_Frame_Range_Manager_Label", text="Label")

        col.separator()
        col.separator()
        col.separator()










        col.prop(self, "PANEL_Object_Action_Manager", text="Object Action Manager Panel")

        if self.PANEL_Object_Action_Manager:
            box = col.box()
            box.prop(self, "PANEL_Object_Action_Manager_Category", text="Category")
            box.prop(self, "PANEL_Object_Action_Manager_Label", text="Label")

        col.separator()
        col.separator()
        col.separator()


        col.prop(self, "PANEL_Action_Baker", text="Action Baker Panel")

        if self.PANEL_Action_Baker:
            box = col.box()
            box.prop(self, "PANEL_Action_Baker_Category", text="Category")
            box.prop(self, "PANEL_Action_Baker_Label", text="Label")
            box.separator()
            box.prop(self, "PANEL_Action_Baker_Show_Action_Selector", text="Show Action Selector")




        col.separator()
        col.separator()
        col.separator()







        col.prop(self, "PANEL_Action_Bin", text="Action Bin Panel")

        if self.PANEL_Action_Bin:
            box = col.box()
            box.prop(self, "PANEL_Action_Bin_Category", text="Category")
            box.prop(self, "PANEL_Action_Bin_Label", text="Label")
            box.prop(self, "PANEL_Action_Bin_Scene_Properties_Panel", text="Scene Properties Panel")
            box.prop(self, "PANEL_Action_Bin_Side_Panel", text="Side Panel")


        col.separator()
        col.separator()
        col.separator()


        col.prop(self, "PANEL_Timeline_Marker_Manager", text="Timeline Marker Manager Panel")

        if self.PANEL_Timeline_Marker_Manager:
            box = col.box()
            box.prop(self, "PANEL_Timeline_Marker_Manager_Category", text="Category")
            box.prop(self, "PANEL_Timeline_Marker_Manager_Label", text="Label")


        col.separator()
        col.separator()
        col.separator()

        col.prop(self, "PANEL_Frame_Remapper", text="Frame Remapper Panel")


        if self.PANEL_Frame_Remapper:
            box = col.box()
            box.prop(self, "PANEL_Frame_Remapper_Category", text="Category")
            box.prop(self, "PANEL_Frame_Remapper_Label", text="Label")
            box.prop(self, "PANEL_Frame_Remapper_Output_Properties_Panel", text="Output Properties Panel")
            box.prop(self, "PANEL_Frame_Remapper_Side_Panel", text="Side Panel")








    def draw_general_options(self, context, layout):

        col = layout.column()

        
        col.label(text="Timeline Utility", icon="TIME")

        box = col.box()

        box.prop(self, "TU_Animation_Player", text="Animation Player")
        box.prop(self, "TU_Frame_Range", text="Frame Range")
        box.prop(self, "TU_Auto_Frame_Range", text="Auto Frame Range")
        col.separator()

        col.label(text="Import Menu", icon="IMPORT")

        box = col.box()

        box.prop(self, "SHOW_IO_Frame_Range", text="Show Frame Range IO Menu")
        box.prop(self, "SHOW_IO_Timeline_Markers", text="Show Timeline Markers IO Menu")

        col.separator()
        box = col.box()

        box.label(text="Extras", icon="SOLO_ON")
        box.prop(self, "ENABLE_Pose_Markers_As_Range", text="Enable Pose Marker As Range Feature")

        box.prop(self, "ENABLE_Action_Operators", text="Enable Action Operators (Experimental)")

       

    def draw(self, context):

        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, "TABS_Preferences", expand=True)

        box = col.box()

        if self.TABS_Preferences == "PANELS":
            self.draw_panel_options(context, box)

        if self.TABS_Preferences == "GENERAL":
            self.draw_general_options(context, box)

        if self.TABS_Preferences == "KEYMAPS":
            keymaps.draw_keymaps(self, context, box)

classes = [FR_Preferences]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    update_panel(None, bpy.context)
    keymaps.set_keymaps()

def unregister():


    unregister_panel(bpy.context)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    keymaps.unset_keymaps()


if __name__ == "__main__":
    register()
