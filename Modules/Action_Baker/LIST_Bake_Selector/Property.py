import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Draw_Helper import Draw_Action_List


def update_bake_to(self, context):
    if self.select_bake_to: 
        if self.bake_to:
            self.bake_to.select_set(True)
            context.view_layer.objects.active = self.bake_to
    
        self.select_bake_to= False 


def update_bake_from(self, context):
    if self.select_bake_from: 
        if self.bake_from:
            self.bake_from.select_set(True)
            context.view_layer.objects.active = self.bake_from 
    
        self.select_bake_from= False 


def set_select_all_action(obj, state):

    if obj:
        action_list_helper = OAM_Functions.Action_List_Helper(obj)
        action_list = action_list_helper.get_action_list() 

        if action_list:
            for slot in action_list:
                slot.select = state 


def select_control_action(self, context):

    if self.select_all_control_action:
        obj = self.bake_from
        set_select_all_action(obj, True)    

        self.select_all_control_action = False


def deselect_control_action(self, context):

    if self.deselect_all_control_action:
        obj = self.bake_from
        set_select_all_action(obj, False)    

        self.deselect_all_control_action = False


def select_deform_action(self, context):

    if self.select_all_deform_action:
        obj = self.bake_to
        set_select_all_action(obj, True)    

        self.select_all_deform_action = False


def deselect_deform_action(self, context):

    if self.deselect_all_deform_action:
        obj = self.bake_to
        set_select_all_action(obj, False)    

        self.deselect_all_deform_action = False

def select_tab_object(self, context):

    if self.select_tab_object:
        
        for obj in context.view_layer.objects:
            obj.select_set(False)

        obj = None

        if self.action_selector_tab == "CONTROL":
            obj = self.bake_from

        if self.action_selector_tab == "DEFORM":
            obj = self.bake_to

        if obj is not None:
            obj.select_set(True)
            context.view_layer.objects.active = obj 


def bake_from_Poll(self, item):

    if item.type == "ARMATURE":
        if not item == self.bake_to:
            return True 

    return False

def bake_to_Poll(self, item):

    if item.type == "ARMATURE":
        if not item == self.bake_from:
            return True 

    return False




ENUM_Action_Selector_Tab = [("CONTROL","Control Armature","Control Armature", "ARMATURE_DATA", 0),("DEFORM","Deform Armature","Deform Armature", "OUTLINER_OB_ARMATURE", 1)]


ENUM_Rename_Mode = [("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix"),("REPLACE","Replace","Replace")]


ENUM_Preclear_Mode = [("PUSH_IF_NON_EXIST","Skip Push if Exist","Skip Push If Exist"), ("ALL", "Clear All NLA Track", "Clear All NLA Track"), ("NONE","None","None")]


class Baker_Property_Group(bpy.types.PropertyGroup):

    show_bake_settings: bpy.props.BoolProperty()
    show_other_options: bpy.props.BoolProperty(default=True)
    show_action_selector: bpy.props.BoolProperty(default=True)
    FR_BAKER_deform_index: bpy.props.IntProperty()
    FR_BAKER_control_index: bpy.props.IntProperty()

    action_selector_tab: bpy.props.EnumProperty(items=ENUM_Action_Selector_Tab, update=select_tab_object)
    select_tab_object: bpy.props.BoolProperty(default=True)

    select_bake_from: bpy.props.BoolProperty(default=False, update=update_bake_from)
    select_bake_to: bpy.props.BoolProperty(default=False, update=update_bake_to)
    
    select_all_control_action: bpy.props.BoolProperty(default=False, update=select_control_action)
    deselect_all_control_action: bpy.props.BoolProperty(default=False, update=deselect_control_action)

    select_all_deform_action: bpy.props.BoolProperty(default=False, update=select_deform_action)
    deselect_all_deform_action: bpy.props.BoolProperty(default=False, update=deselect_deform_action)



    select_all_action: bpy.props.BoolProperty(default=False)
    deselect_all_action: bpy.props.BoolProperty(default=False)


    Pre_Unmute: bpy.props.BoolProperty(default=True)
    Post_Mute: bpy.props.BoolProperty(default=True)

    bake_from: bpy.props.PointerProperty(type=bpy.types.Object, poll=bake_from_Poll)
    bake_to: bpy.props.PointerProperty(type=bpy.types.Object, poll=bake_to_Poll)

    bake_show_popup: bpy.props.BoolProperty(default=True)




    push_to_nla: bpy.props.BoolProperty(default=False)
    preclear_nla: bpy.props.EnumProperty(items=ENUM_Preclear_Mode)

    load_to_slot: bpy.props.BoolProperty(default=True)
    preclear_slots: bpy.props.BoolProperty(default=False)

    overwrite: bpy.props.BoolProperty(default=False)




    only_selected: bpy.props.BoolProperty()
    visual_keying: bpy.props.BoolProperty(default=True)
    clear_constraint: bpy.props.BoolProperty()
    clear_parent: bpy.props.BoolProperty()
    clean_curve: bpy.props.BoolProperty()
    bake_pose: bpy.props.BoolProperty(default=True)
    bake_object: bpy.props.BoolProperty(default=False)

    show_rename_settings: bpy.props.BoolProperty()
    rename_mode: bpy.props.EnumProperty(items=ENUM_Rename_Mode)
    string_a: bpy.props.StringProperty(default="Baked_")
    string_b: bpy.props.StringProperty()

    use_bake_name_when_available: bpy.props.BoolProperty(default=True)

    def draw_rename_settings(self, layout):
    
        box = layout

        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(self, "rename_mode", expand=True) 

        if self.rename_mode == "REPLACE":
            col.prop(self, "string_a", text="From") 
            col.prop(self, "string_b", text="To") 

        if self.rename_mode == "SUFFIX":
            col.prop(self, "string_a", text="Suffix") 

        if self.rename_mode == "PREFIX":
            col.prop(self, "string_a", text="Prefix") 

        col.prop(self, "use_bake_name_when_available", text="Use Bake Name When Available") 

    def draw_action_selector(self, context, layout):
        box = layout.box()

        if Utility_Function.draw_subpanel(box, "Action Selector", self, "show_action_selector"):
            row = box.row(align=True)
            row.prop(self, "action_selector_tab", expand=True)
            row.prop(self, "select_tab_object", icon="RESTRICT_SELECT_OFF", text="")

            if self.action_selector_tab == "CONTROL":
                control_armature = self.bake_from

                if control_armature is not None:
                    col = box.column(align=True)


                    Draw_Action_List.MENU_OBJECT = self.bake_from
                    Draw_Action_List.draw_list(col, context, control_armature, draw_strip=True, draw_action_counter=True)

                    # col.popover(panel="FR_PT_Action_Bin_Adder_control", text="Action Bin", icon="PLUS")
                    # row = col.row()
                    # row.template_list("FR_UL_BAKER_List", "", control_armature, "OAM", control_armature, "OAM_Index")
                    # self.Draw_Listbox_Operators(bpy.context, row, control_armature)
                    #
                    row = box.row(align=True)
                    row.prop(self, "select_all_control_action", text="Select All", icon="RESTRICT_SELECT_ON")
                    row.prop(self, "deselect_all_control_action", text="Deselect All", icon="RESTRICT_SELECT_OFF")

                else:
                    box.label(text="Select Control Armature", icon="INFO")
                
            if self.action_selector_tab == "DEFORM":
                deform_armature = self.bake_to

                if deform_armature is not None:
                    col = box.column(align=True)


                    icon_expose_menu_id = "ACTIONLIST_MT_icon_expose" 

                    Draw_Action_List.MENU_OBJECT = self.bake_to
                    Draw_Action_List.draw_list(col, context, deform_armature, draw_strip=True, draw_action_counter=True)

                    # col.popover(panel="FR_PT_Action_Bin_Adder_deform", text="Action Bin", icon="PLUS")
                    # row = col.row()
                    # row.template_list("FR_UL_BAKER_List", "", deform_armature, "OAM", deform_armature, "OAM_Index")
                    # self.Draw_Listbox_Operators(bpy.context, row, deform_armature)
                    #
                    row = box.row(align=True)
                    row.prop(self, "select_all_deform_action", text="Select All", icon="RESTRICT_SELECT_ON")
                    row.prop(self, "deselect_all_deform_action", text="Deselect All", icon="RESTRICT_SELECT_OFF")
                




                else:
                    box.label(text="Select Deform Armature", icon="INFO")

    def draw_basic_settings(self, layout):

        layout.prop(self, "overwrite", text="Overwrite")
        layout.prop(self, "Post_Mute", text="Post Mute Constraint")
        layout.prop(self, "Pre_Unmute", text="Pre Unmute Constraint")
        layout.prop(self, "push_to_nla", text="Push To NLA")

        if self.push_to_nla:
            box = layout.box()
            box.prop(self, "preclear_nla", text="Pre Clear NLA")

        layout.prop(self, "load_to_slot", text="Load To Action Slot")

        if self.load_to_slot:

            box = layout.box()
            box.prop(self, "preclear_slots", text="Pre Clear Slot")

    def draw(self, context, layout):

        preferences = Utility_Function.get_addon_preferences()

        if preferences.PANEL_Action_Baker_Show_Action_Selector:
            self.draw_action_selector(context, layout)



        row = layout.row(align=True)
        row.prop(self, "bake_from", text="Control")
        if self.bake_from:
            row.prop(self, "select_bake_from", text="", icon="RESTRICT_SELECT_OFF")
        row = layout.row(align=True)
        row.prop(self, "bake_to", text="Deform")
        if self.bake_from:
            row.prop(self, "select_bake_to", text="", icon="RESTRICT_SELECT_OFF")
   


        row = layout.row(align=True)
        row.operator("fr_baker.toogle_constraint", text="Mute Constraint", icon="HIDE_ON").mute = True
        row.operator("fr_baker.toogle_constraint", text="Unmute Constraint", icon="HIDE_OFF").mute = False 
        layout.separator()

        # if not self.bake_to:
        #     box = layout.box()
        #     box.label(text="Select Deform Armature", icon="ERROR")
        #     
        # if not self.bake_from:
        #     box = layout.box()
        #     box.label(text="Select Control Armature", icon="ERROR")



        # self.draw_basic_settings(layout)

        bake_enable = False 


        if self.bake_from and self.bake_to:
            if self.bake_from == self.bake_to:
                box = layout.box()
                box.label(text="Control Rig and Deform Rig Are Same", icon="ERROR")
            else:
                bake_enable = True
    
        if not self.bake_from or not self.bake_to:
            box = layout.box()
        if not self.bake_from:
            box.label(text="Select Control Armature", icon="INFO")
        if not self.bake_to:
            box.label(text="Select Control Deform", icon="INFO")


        row = layout.row(align=True)
        row.enabled = bake_enable
        row.operator("fr_baker.bake_deform_armature", text="Bake Deform Armature", icon="KEYTYPE_KEYFRAME_VEC")
        row.prop(self, "bake_show_popup", text="", icon="SETTINGS")

        layout.separator()


        box = layout.box()
        if Utility_Function.draw_subpanel(box, "Settings", self, "show_bake_settings"):

            box.label(text="Rename Settings")
            box2 = box.box()
            self.draw_rename_settings(box2)

            box.label(text="Basic Settings")
            box2 = box.box()
            self.draw_basic_settings(box2)

            box.label(text="Bake Settings")
            box2 = box.box()
            self.draw_bake_settings(box2)


    def draw_bake_settings(self, layout):


        layout.prop(self, "only_selected", text="Only Selected Bone")
        layout.prop(self, "visual_keying", text="Visual Keying")
        layout.prop(self, "clear_constraint", text="Clear Constraint")
        layout.prop(self, "clear_parent", text="Clear Parent")
        layout.prop(self, "clean_curve", text="Clean Curve")
        layout.prop(self, "bake_pose", text="Bake Pose")
        layout.prop(self, "bake_object", text="Bake Object")
        

    def Draw_Listbox_Operators(self, context, layout, obj):

        scn = context.scene
        Baker = scn.FR_BAKER
        deform = Baker.bake_to 
        control = Baker.bake_from


        index = obj.OAM_Index
        col = layout.column(align=True)

        target_object = None

        if obj == deform:
            target_object = "DEFORM"

        if obj == control:
            target_object = "CONTROL"

        operator = col.operator("fr_oam.add_action_slot", text="", icon = "ADD")
        operator.Load_Action = False
        operator.Load_Action_Name = ""
        operator.target_object = target_object 

        # col.operator("fr_oam.remove_action_slot", text="", icon = "REMOVE").Index = index
        operator = col.operator("fr_oam.remove_action_slot", text="", icon = "REMOVE")
        operator.Index = index
        operator.target_object = target_object 
        col.separator()

        col.menu("OBJECT_MT_fr_baker_icon_expose", icon="VIS_SEL_11", text="")
        col.menu("OBJECT_MT_fr_oam_extra", icon="DOWNARROW_HLT", text="")

        col.separator()
        reorder_Up = col.operator("fr_oam.reorder_action_slot", text="", icon = "TRIA_UP")
        reorder_Up.Index = obj.OAM_Index
        reorder_Up.Mode = "UP"
        reorder_Up.target_object = target_object

        reorder_Down = col.operator("fr_oam.reorder_action_slot", text="", icon = "TRIA_DOWN")
        reorder_Down.Index = obj.OAM_Index
        reorder_Down.Mode = "DOWN"
        reorder_Down.target_object = target_object 







classes = [Baker_Property_Group]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Scene.FR_BAKER = bpy.props.PointerProperty(type=Baker_Property_Group)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



    del bpy.types.Scene.FR_BAKER



if __name__ == "__main__":

    register()

