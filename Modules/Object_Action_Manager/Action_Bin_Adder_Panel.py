
from Frame_Ranger import Utility_Function
from bpy.types import Preferences
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Draw_Helper import Draw_Action_List

import bpy



def draw_action_bin_adder(self, context, obj):
    layout = self.layout
    scn = context.scene

    preferences = Utility_Function.get_addon_preferences()

    actions = bpy.data.actions
    
    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(preferences, "ABA_Filter", text="", icon="VIEWZOOM")
    row = col.row(align=True)
    row.prop(preferences, "ABA_Filter_Mode", expand=True)
       
    operator = layout.operator("fr_oam.load_all_action", text="Load All Actions", icon="TRIA_DOWN_BAR")
    operator.target_object = obj.name 
    operator.filter = preferences.ABA_Filter
    operator.filter_mode = preferences.ABA_Filter_Mode
    operator.show_options = False


    size = 0

    for index, action in enumerate(actions):


        scn = context.scene


        if obj:
            
            obj_name = obj.name

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            has_action = action_list_helper.has_action(action)
            
            if not has_action:
               
                show = Utility_Function.filter_action(preferences.ABA_Filter, preferences.ABA_Filter_Mode, action.name)

                if show:
                    row = layout.row()
                    row.alignment="LEFT"
                    operator = row.operator("fr_oam.load_action_slot", text=action.name, icon = "ADD", emboss=False)
                    operator.load_action_name = action.name
                    operator.target_object = obj_name
                    operator.show_options = False
                    size += 1






    if size == 0:
        layout.label(text="No Action Found", icon="INFO")


class FR_PT_Action_Adder_Panel(bpy.types.Panel):
    bl_label = "Object Action Manager"
    bl_idname = "FR_PT_Action_Bin_Adder"
    bl_options = {"INSTANCED"}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'


    @classmethod
    def poll(cls, context):
        return True
    def draw(self, context):

        obj = Draw_Action_List.ACTION_BIN_OBJECT
        draw_action_bin_adder(self, context, obj=obj)




classes = [FR_PT_Action_Adder_Panel]


def register():


    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():


    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
 register()
