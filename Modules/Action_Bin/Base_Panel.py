import bpy

from Frame_Ranger import Utility_Function

class FR_PT_Action_Bin_Base(bpy.types.Panel):
    bl_label = "Action Bin"


    def Draw_List(self, context, layout):
        scn = context.scene
        layout.template_list("FR_UL_Action_Bin", "", bpy.data, "actions", scn, "AB_Index")

    def Draw_List_Operator(self, context, layout):

        scn = context.scene

        col = layout.column(align=True)
        col.operator("fr_ab.add_action", text="", icon = "ADD")
        col.operator("fr_ab.remove_action", text="", icon = "REMOVE").index = scn.AB_Index
        col.separator()
        col.menu("OBJECT_MT_fr_ab_icon_expose", icon="VIS_SEL_11", text="")
        col.menu("OBJECT_MT_fr_ab_extra", icon="DOWNARROW_HLT", text="")


    def draw(self, context):
        
        scn = context.scene
        layout = self.layout

        preferences = Utility_Function.get_addon_preferences()

        row = layout.row()
        self.Draw_List(context, row)
        self.Draw_List_Operator(context, row)
        self.Draw_Action_Settings(context, layout)

    def Draw_Action_Settings(self, context, layout):
       
        scn = context.scene
        index = scn.AB_Index

        if len(bpy.data.actions) > index:
            action = bpy.data.actions[index]


            if action:

                layout = layout.box() 
                row = layout.row(align=True)

                preferences = Utility_Function.get_addon_preferences()
                show_settings =  Utility_Function.draw_subpanel(row, "", preferences, "OAM_SHOW_Action_Bin_Settings")

                row.prop(action, "name", text="")

                row.operator("fr_ab.duplicate_action", text="", icon = "DUPLICATE").index = index

                row.prop(action, "use_fake_user", text="")
                row.operator("fr_ab.remove_action", text="", icon = "X").index = index

                row = layout.row(align=True)

                if show_settings: 


                    if action.use_frame_range:

                        row.prop(action, "frame_start", text="Start", index = 0)
                        row.prop(action, "frame_end", text="End", index = 1)

                        # row.operator("fr_ab.match_range_to_keyframe", text="", icon = "COPYDOWN").Index = obj.OAM_Index
                        # row.separator()
                    
                    else:
                        row.prop(action, "curve_frame_range", text="Start", index = 0)
                        row.prop(action, "curve_frame_range", text="End", index = 1)

                    row = layout.row(align=True)
                    row.prop(action, "use_frame_range", text="Manual Frame Range")
                    row.prop(action, "use_cyclic", text="Use Cyclic")





