import bpy
from Frame_Ranger import Utility_Function


class FR_UL_Frame_Range_Manager_List(bpy.types.UIList):


    # def filter_items(self, context, data, propname):
    #
    #     filtered = []
    #     ordered = []
    #     items = getattr(data, propname)
    #
    #     filtered = [self.bitflag_filter_item] * len(items)
    #
    #     for i, item in enumerate(items):
    #         if not self.filter_name == "":
    #             if not self.filter_name in item.name:
    #                 filtered[i] &= ~self.bitflag_filter_item
    #
    #     return filtered, ordered



    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        scn = context.scene
        ob = data
        row = layout.row(align=True)

        preferences = Utility_Function.get_addon_preferences()


        if preferences.FRM_ICON_Set_Range:
            row.operator("fr_frm.set_frame_range", text="", icon="TIME").index = index

        row.prop(item, "name", text="", emboss=False)

        row = layout.row(align=True)
        row.alignment="RIGHT"

        if preferences.FRM_ICON_Frame_Range:
            row.prop(item, "Start", text="", emboss=True)
            row.prop(item, "End", text="", emboss=True)


        if preferences.FRM_ICON_Remove:
            row.operator("fr_frm.remove_frame_range", text="", icon="TRASH").index = index



class FR_UL_Frame_Range_Set_List(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        scn = context.scene
        ob = data
        row = layout.row(align=True)

        preferences = Utility_Function.get_addon_preferences()

        row.prop(item, "name", text="", emboss=False)

        if preferences.FRS_ICON_Remove:
            row.operator("fr_frm.remove_frame_range_set", text="", icon = "TRASH").index = index






classes = [FR_UL_Frame_Range_Set_List, FR_UL_Frame_Range_Manager_List]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
